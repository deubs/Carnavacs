namespace Carnavacs.Api.Domain.Entities
{
    /// <summary>
    /// Request model for Quentro API validate/check endpoints
    /// </summary>
    public record QuentroTicketRequest(
        string Code,
        int[] Sectors,
        string Gate
    );

    /// <summary>
    /// Response model from Quentro API validate/check endpoints
    /// </summary>
    public class QuentroTicketResponse
    {
        public bool Valid { get; set; }
        public string? Message { get; set; }
        public string? M1 { get; set; }
        public string? M2 { get; set; }
        public string? Status { get; set; }
        public string? TicketType { get; set; }
        public string? HolderName { get; set; }
        
        /// <summary>
        /// When the ticket was used (returned when status is USED)
        /// </summary>
        public string? UsedDate { get; set; }
        
        /// <summary>
        /// Gate where the ticket was used
        /// </summary>
        public string? Gate { get; set; }
        
        /// <summary>
        /// Whether the current validation is from the same gate where it was originally used
        /// </summary>
        public bool? SameGate { get; set; }
        
        /// <summary>
        /// Error code from Quentro API (e.g., 401 for used tickets)
        /// </summary>
        public int? ErrorCode { get; set; }
        
        /// <summary>
        /// Code returned in error responses (e.g., "USED")
        /// </summary>
        public string? Code { get; set; }
    }
}
