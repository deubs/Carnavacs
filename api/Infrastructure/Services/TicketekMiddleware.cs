using Azure;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Domain.Entities.Ticketek;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using Microsoft.Data.SqlClient;

namespace Carnavacs.Api.Infrastructure.Services
{
    public class TicketekMiddleware : BackgroundService
    {
        private readonly ILogger<TicketekMiddleware> _logger;
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _configuration;
        private readonly string _connectionString;
        private readonly IServiceScopeFactory _scopeFactory;

        public TicketekMiddleware(
            ILogger<TicketekMiddleware> logger,
            IHttpClientFactory httpClientFactory,
            IConfiguration configuration, IServiceScopeFactory scopeFactory)
        {
            _logger = logger;
            _httpClientFactory = httpClientFactory;
            _configuration = configuration;
            _connectionString = configuration.GetConnectionString("Carnaval");
            _scopeFactory = scopeFactory;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {

            bool sync = _configuration.GetValue<bool>("TicketApi:Sync");
            while (!stoppingToken.IsCancellationRequested && sync)
            {
                try
                {
                    await ProcessAllTicketPagesAsync();
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error occurred while processing tickets");
                }finally
                {
                    await Task.Delay(TimeSpan.FromSeconds(1), stoppingToken);
                }
            }
        }

        private async Task ProcessAllTicketPagesAsync()
        {
            string nextId = null;
            int processedPages = 0;
            int totalTicketsProcessed = 0;
            int remainingPages = 1;
            bool hasMorePages = true;

            using (var scope = _scopeFactory.CreateScope())
            {
                var _unitOfWork = scope.ServiceProvider.GetRequiredService<IUnitOfWork>();
                Event evt = await _unitOfWork.Events.GetCurrentAsync();
                DateTime lastUpdate = _unitOfWork.Tickets.GetLastSync(evt.ShowName);

                while (hasMorePages) { 
                    var response = await FetchTicketsPageAsync(evt.ShowName, lastUpdate, nextId);
                    if (response == null || !response.Tickets.Any())
                    {
                        hasMorePages = false;
                        break;
                    } 

                    await ProcessTicketBatchAsync(response.Tickets);

                    totalTicketsProcessed += response.Tickets.Count;
                    processedPages++;
                    remainingPages = response.RemainingPages - processedPages;
                    hasMorePages = response.RemainingTickets > 0;

                    _logger.LogInformation(
                        "Processed page {Page} with {TicketCount} tickets. Total processed: {TotalTickets}. Remaining pages: {RemainingPages}",
                        processedPages,
                        response.Tickets.Count,
                        totalTicketsProcessed,
                        response.RemainingPages
                    );

                    nextId = response.LastId;
                } while (nextId != null && remainingPages > 0);
            }
            _logger.LogInformation(
                "Completed processing {TotalPages} pages with {TotalTickets} tickets total",
                processedPages,
                totalTicketsProcessed
            );
        }

        private async Task<ApiResponse> FetchTicketsPageAsync(string showName, DateTime lastUpdate, string nextId)
        {
            using var client = _httpClientFactory.CreateClient("TicketApi");
            var apiKey = _configuration["TicketApi:ApiKey"];
            var baseUrl = _configuration["TicketApi:BaseUrl"];
            var url = $"{baseUrl}?showname={showName}&updatedAt_gte={lastUpdate.ToString("yyyy/MM/dd HH:mm")}";
            url += nextId == null ? "" : $"&_id_next={nextId}";

            try
            {
                client.DefaultRequestHeaders.Add("x-api-key", apiKey);
                return await client.GetFromJsonAsync<ApiResponse>(url);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error fetching tickets page with nextId: {NextId}", nextId);
                throw;
            }
        }


        private async Task ProcessTicketBatchAsync(List<Carnavacs.Api.Domain.Entities.Ticketek.Ticket> tickets)
        {
            var connection = new SqlConnection(_connectionString);
            foreach (var ticket in tickets)
            {
                _logger.LogInformation($"{ticket}");
                try
                {
                    var sql = @"
                    MERGE INTO TicketekTickets AS target
                    USING (SELECT @Id AS Id) AS source
                    ON target.Id = source.Id
                    WHEN NOT MATCHED THEN
                        INSERT (Id, Event, Sequence, Barcode, CreatedAt, Dlvy_type, Mjt, 
                                Price_type, Row, Seat, Section, Showname, Status, UpdatedAt)
                        VALUES (@Id, @Event, @Sequence, @Barcode, @CreatedAt, @Dlvy_type, @Mjt,
                                @Price_type, @Row, @Seat, @Section, @Showname, @Status, @UpdatedAt)
                    WHEN MATCHED AND target.UpdatedAt < @UpdatedAt THEN
                        UPDATE SET 
                            Event = @Event,
                            Sequence = @Sequence,
                            Barcode = @Barcode,
                            Dlvy_type = @Dlvy_type,
                            Mjt = @Mjt,
                            Price_type = @Price_type,
                            Row = @Row,
                            Seat = @Seat,
                            Section = @Section,
                            Showname = @Showname,
                            Status = @Status,
                            UpdatedAt = @UpdatedAt;";

                    var parameters = new
                    {
                        Id = ticket._id,
                        ticket.Event,
                        ticket.Sequence,
                        ticket.Barcode,
                        ticket.CreatedAt,
                        ticket.Dlvy_type,
                        ticket.Mjt,
                        ticket.Price_type,
                        ticket.Row,
                        ticket.Seat,
                        ticket.Section,
                        ticket.Showname,
                        ticket.Status,
                        ticket.UpdatedAt
                    };

                    await connection.ExecuteAsync(sql, parameters);
                    _logger.LogInformation("Processed ticket: {Id}", ticket._id);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error processing ticket {Id}", ticket._id);
                }
            }

            return;
        }
    }
}
