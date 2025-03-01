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
        /// Validate ticket and mark it as used, if persist is true, the ticket will be saved. 
        /// </summary>
        /// <param name="code">ticket code. a barcode or qr scan</param>
        /// <returns>Validation result</returns>
        Task<TicketValidationResult> ValidateAsync(string code);
    }
}
