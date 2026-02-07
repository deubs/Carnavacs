using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Net.Http.Json;
using System.Text.Json;

namespace Carnavacs.Api.Infrastructure.Services
{
    /// <summary>
    /// HTTP client for Quentro Box ticket validation API
    /// </summary>
    public class QuentroApiClient : IQuentroApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<QuentroApiClient> _logger;
        private readonly DapperContext _dbContext;
        private readonly string[] _servers;

        // Cache for Quentro credentials and sectors (valid for the entire event day)
        private static string? _cachedShowId;
        private static string? _cachedShowKey;
        private static int[]? _cachedSectorIds;
        private static DateTime _cacheDate = DateTime.MinValue;
        private static readonly object _cacheLock = new();

        // Round-robin server index
        private static int _serverIndex = 0;

        private static readonly JsonSerializerOptions JsonOptions = new()
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };

        public QuentroApiClient(HttpClient httpClient, IConfiguration configuration, ILogger<QuentroApiClient> logger, DapperContext dbContext)
        {
            _httpClient = httpClient;
            _logger = logger;
            _dbContext = dbContext;
            _servers = configuration.GetSection("QuentroApi:Servers").Get<string[]>()
                ?? throw new InvalidOperationException("QuentroApi:Servers not configured");

            if (_servers.Length == 0)
                throw new InvalidOperationException("QuentroApi:Servers must have at least one server");
        }

        private string GetNextServer()
        {
            var index = Interlocked.Increment(ref _serverIndex) % _servers.Length;
            return _servers[index];
        }

        private async Task<(string showId, string showKey)> GetCredentialsAsync()
        {
            var today = DateTime.Today;

            lock (_cacheLock)
            {
                if (_cacheDate == today && !string.IsNullOrEmpty(_cachedShowId) && !string.IsNullOrEmpty(_cachedShowKey))
                {
                    return (_cachedShowId, _cachedShowKey);
                }
            }

            using var connection = _dbContext.CreateConnection();
            var query = @"SELECT TOP 1 ev.QuentroEventId, ev.QuentroEventKey
                          FROM Eventos ev
                          INNER JOIN Espectaculos e ON ev.EspectaculoFk = e.Id
                          WHERE ev.Habilitado = 1 AND e.Habilitado = 1 AND ev.FechaFin > @now
                          ORDER BY ev.Fecha";

            var result = await connection.QueryFirstOrDefaultAsync<(string? QuentroEventId, string? QuentroEventKey)>(
                query, new { now = DateTime.Now });

            if (string.IsNullOrEmpty(result.QuentroEventId) || string.IsNullOrEmpty(result.QuentroEventKey))
            {
                throw new InvalidOperationException("Quentro credentials not configured for current event");
            }

            lock (_cacheLock)
            {
                _cachedShowId = result.QuentroEventId;
                _cachedShowKey = result.QuentroEventKey;
                _cacheDate = today;
            }

            _logger.LogInformation("Loaded Quentro credentials for event, ShowId: {ShowId}", result.QuentroEventId);
            return (result.QuentroEventId, result.QuentroEventKey);
        }

        private async Task<int[]> GetSectorsAsync(string showId, string showKey)
        {
            lock (_cacheLock)
            {
                if (_cachedSectorIds != null && _cachedSectorIds.Length > 0)
                {
                    return _cachedSectorIds;
                }
            }

            // Try each server with failover
            for (int i = 0; i < _servers.Length; i++)
            {
                var server = GetNextServer();
                try
                {
                    var request = new HttpRequestMessage(HttpMethod.Get, $"{server}/sectors");
                    request.Headers.Add("X-Quentro-Show", showId);
                    request.Headers.Add("X-Quentro-ShowKey", showKey);

                    var response = await _httpClient.SendAsync(request);
                    response.EnsureSuccessStatusCode();

                    var result = await response.Content.ReadFromJsonAsync<QuentroSectorsResponse>(JsonOptions);
                    var sectorIds = result?.Sectors?.Select(s => s.Id).ToArray() ?? [];

                    if (sectorIds.Length > 0)
                    {
                        lock (_cacheLock)
                        {
                            _cachedSectorIds = sectorIds;
                        }
                        _logger.LogInformation("Loaded {Count} sectors from Quentro API ({Server})", sectorIds.Length, server);
                    }

                    return sectorIds;
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Error fetching sectors from Quentro API ({Server}), trying next server", server);
                }
            }

            _logger.LogError("All Quentro API servers failed when fetching sectors");
            return [];
        }

        public async Task<QuentroTicketResponse?> ValidateAsync(string code, int[]? sectors = null, string? gate = null)
        {
            return await SendRequestAsync("validate", code, sectors, gate);
        }

        public async Task<QuentroTicketResponse?> CheckAsync(string code, int[]? sectors = null, string? gate = null)
        {
            return await SendRequestAsync("check", code, sectors, gate);
        }

        private async Task<QuentroTicketResponse?> SendRequestAsync(string endpoint, string code, int[]? sectors, string? gate)
        {
            var (showId, showKey) = await GetCredentialsAsync();
            sectors ??= await GetSectorsAsync(showId, showKey);

            // Try each server with failover
            for (int i = 0; i < _servers.Length; i++)
            {
                var server = GetNextServer();
                try
                {
                    var request = new HttpRequestMessage(HttpMethod.Post, $"{server}/{endpoint}");
                    request.Headers.Add("X-Quentro-Show", showId);
                    request.Headers.Add("X-Quentro-ShowKey", showKey);

                    var body = new QuentroTicketRequest(code, sectors, gate ?? "API");
                    request.Content = JsonContent.Create(body, options: JsonOptions);

                    var response = await _httpClient.SendAsync(request);

                    // On 404, try next server (ticket might exist on other server)
                    if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                    {
                        _logger.LogWarning("Quentro API ({Server}) returned 404 for code {Code}, trying next server", server, code);
                        continue;
                    }

                    // Always try to parse the response body - even error responses contain useful info
                    // (e.g., USED tickets return error code but include usedDate, gate, etc.)
                    var result = await response.Content.ReadFromJsonAsync<QuentroTicketResponse>(JsonOptions);

                    if (!response.IsSuccessStatusCode)
                    {
                        _logger.LogWarning("Quentro API ({Server}) returned {StatusCode} for code {Code}: {Status}",
                            server, response.StatusCode, code, result?.Status ?? result?.Code);

                        // Still return the result so we can extract usage info
                        if (result != null)
                        {
                            result.Valid = false;
                        }
                    }

                    return result;
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Error calling Quentro API ({Server}) for code {Code}, trying next server", server, code);
                }
            }

            _logger.LogError("All Quentro API servers failed for code {Code}", code);
            return new QuentroTicketResponse
            {
                Valid = false,
                Status = "NOT_FOUND",
                M1 = "ENTRADA",
                M2 = "NO ENCONTRADA"
            };
        }
    }
}
