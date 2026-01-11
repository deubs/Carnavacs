using Carnavacs.Api.Domain.Entities;

namespace Carnavacs.Api.Infrastructure.Interfaces
{
    public interface ITicketRepository : IRepository<Ticket>
    {
        DateTime GetLastSync(string evt);

        /// <summary>
        /// Mark ticket as used, or count retry if already used
        /// </summary>
        /// <param name="code">Ticket code (barcode or qr)</param>
        /// <returns></returns>
        Task UseAsync(string code, string? device);

        /// <summary>
        /// Log a Quentro ticket validation (ticket already burned by Quentro API)
        /// </summary>
        /// <param name="code">Quentro ticket code</param>
        /// <param name="device">Device identifier that read the ticket</param>
        /// <param name="status">The ticket status from validation</param>
        /// <param name="ticketType">Ticket type/sector from Quentro API</param>
        Task LogQuentroAsync(string code, string? device, TicketStatus status, string? ticketType = null);

        /// <summary>
        /// Validate ticket and mark it as used, if persist is true, the ticket will be saved. 
        /// </summary>
        /// <param name="code">ticket code. a barcode or qr scan</param>
        /// <param name="readOnly">If true, only check validity without marking as used (for Quentro API)</param>
        /// <param name="deviceId">Device/gate identifier to pass to Quentro API</param>
        /// <returns>Validation result</returns>
        Task<TicketValidationResult> ValidateAsync(string code, bool readOnly = false, string? deviceId = null);
    }
}
