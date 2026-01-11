using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
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
        private readonly string _baseUrl;
        private readonly string _showId;
        private readonly string _showKey;

        private static readonly JsonSerializerOptions JsonOptions = new()
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };

        public QuentroApiClient(HttpClient httpClient, IConfiguration configuration, ILogger<QuentroApiClient> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
            _baseUrl = configuration["QuentroApi:BaseUrl"] ?? throw new InvalidOperationException("QuentroApi:BaseUrl not configured");
            _showId = configuration["QuentroApi:ShowId"] ?? throw new InvalidOperationException("QuentroApi:ShowId not configured");
            _showKey = configuration["QuentroApi:ShowKey"] ?? throw new InvalidOperationException("QuentroApi:ShowKey not configured");
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
            try
            {
                sectors = new int[] {

  35853899, 35828248, 35828247, 35828246, 35828245, 35828244, 35828243, 35828242,
  35828241, 35828240, 35828239, 35828238, 35828237, 35828236, 35828235, 35828234,
  35828233, 35828232, 35828231, 35828230, 35828229, 35828228, 35828227, 35828226,
  35828225, 35828224, 35828223, 35828222, 35828221, 35828220, 35828219, 35828218,
  35828217, 35828216, 35828215, 35828214, 35828213, 35828212, 35828211, 35828210,
  35828209, 35828208, 35828207, 35828206, 35828205, 35828204, 35828203, 35828202,
  35828201, 35828200, 35828199, 35828198, 35828197, 35828196, 35828195, 35828194,
  35828193, 35828192, 35828191, 35828190, 35828189, 35828188, 35828187, 35828186,
  35828185, 35828184, 35828183, 35828182, 35828181, 35828180, 35828179, 35828178,
  35828177, 35828176, 35828175, 35828174, 35828173, 35828172, 35828171, 35828170,
  35828169, 35828168, 35828167, 35828166, 35828165, 35828164, 35828163, 35828162,
  35828161, 35828160, 35828159, 35828158, 35828157, 35828156, 35828155, 35828154,
  35828153, 35828152, 35828151, 35828150, 35828149, 35828148, 35828147, 35828146,
  35828145, 35828144, 35828143, 35828142, 35828141, 35828140, 35828139, 35828138,
  35828137, 35828136, 35828135, 35828134, 35828133, 35828132, 35828131, 35828130,
  35828129, 35828128, 35828127, 35828126, 35828125, 35828124, 35828123, 35828122,
  35828121, 35828120, 35828119, 35828118, 35828117, 35828116, 35828115, 35828114,
  35828113, 35828112, 35828111, 35828110, 35828109, 35828108, 35828107, 35828106,
  35828105, 35828104, 35828103, 35828102
                };

                var request = new HttpRequestMessage(HttpMethod.Post, $"{_baseUrl}/{endpoint}");
                request.Headers.Add("X-Quentro-Show", _showId);
                request.Headers.Add("X-Quentro-ShowKey", _showKey);

                var body = new QuentroTicketRequest(code, sectors ?? [1211], gate ?? "API");
                request.Content = JsonContent.Create(body, options: JsonOptions);

                var response = await _httpClient.SendAsync(request);
                
                // Always try to parse the response body - even error responses contain useful info
                // (e.g., USED tickets return error code but include usedDate, gate, etc.)
                var result = await response.Content.ReadFromJsonAsync<QuentroTicketResponse>(JsonOptions);
                
                if (!response.IsSuccessStatusCode)
                {
                    _logger.LogWarning("Quentro API returned {StatusCode} for code {Code}: {Status}", 
                        response.StatusCode, code, result?.Status ?? result?.Code);
                    
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
                _logger.LogError(ex, "Error calling Quentro API for code {Code}", code);
                return null;
            }
        }
    }
}
