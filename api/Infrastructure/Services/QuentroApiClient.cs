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
  35853895, 35828101, 35826526, 35826433, 35826432, 35826431, 35826430,
  35826429, 35826428, 35826427, 35826426, 35826425, 35826424, 35826423,
  35826422, 35826421, 35826420, 35826419, 35826418, 35826417, 35826416,
  35826415, 35826414, 35826413, 35826412, 35826411, 35826410, 35826409,
  35826408, 35826407, 35826406, 35826405, 35826404, 35826403, 35826402,
  35826401, 35826400, 35826399, 35826398, 35826397, 35826396, 35826395,
  35826394, 35826393, 35826392, 35826391, 35826390, 35826389, 35826388,
  35826387, 35826386, 35826385, 35826384, 35826383, 35826382, 35826381,
  35826380, 35826379, 35826378, 35826377, 35826376, 35826375, 35826374,
  35826373, 35826372, 35826371, 35826370, 35826369, 35826368, 35826367,
  35826366, 35826365, 35826364, 35826363, 35826362, 35826361, 35826360,
  35826359, 35826358, 35826357, 35826356, 35826355, 35826354, 35826353,
  35826352, 35826351, 35826350, 35826349, 35826348, 35826347, 35826346,
  35826345, 35826344, 35826343, 35826342, 35826341, 35826340, 35826339,
  35826338, 35826337, 35826336, 35826335, 35826334, 35826333, 35826332,
  35826331, 35826330, 35826329, 35826328, 35826327, 35826326, 35826325,
  35826324, 35826323, 35826322, 35826321, 35826320, 35826319, 35826318,
  35826317, 35826316, 35826315, 35826314, 35826313, 35826312, 35826311,
  35826310, 35826309, 35826308, 35826307, 35826306, 35826305, 35826304,
  35826303, 35826302, 35826301, 35826300, 35826299, 35826298, 35826297,
  35826296, 35826295, 35826294, 35826293, 35826292, 35826291, 35826290,
  35826289, 35826288, 35826287, 35826286
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
