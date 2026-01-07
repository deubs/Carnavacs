using Carnavacs.Api.Domain.Entities;

namespace Carnavacs.Api.Infrastructure.Interfaces
{
    /// <summary>
    /// Client for Quentro Box ticket validation API
    /// </summary>
    public interface IQuentroApiClient
    {
        /// <summary>
        /// Validates a ticket code and marks it as used
        /// </summary>
        Task<QuentroTicketResponse?> ValidateAsync(string code, int[]? sectors = null, string? gate = null);

        /// <summary>
        /// Checks a ticket code without marking it as used (read-only)
        /// </summary>
        Task<QuentroTicketResponse?> CheckAsync(string code, int[]? sectors = null, string? gate = null);
    }
}
