using System.Text.Json.Serialization;

namespace Carnavacs.Api.Domain.Entities
{
    public class TicketValidationResult
    {
        public string M1 { get; set; }
        public string M2 { get; set; }

        public TicketStatus TicketStatus { get; set; } = TicketStatus.NotFound;
        public int TicketId { get; set; } = 0;
        public bool IsValid => TicketStatus == TicketStatus.OK;
        public bool Exists => TicketStatus != TicketStatus.NotFound;
        
        /// <summary>
        /// Date/time when the ticket was used (for used tickets)
        /// </summary>
        public string? UsedDate { get; set; }
        
        /// <summary>
        /// Gate where the ticket was used (for used tickets)
        /// </summary>
        public string? Gate { get; set; }

        /// <summary>
        /// Indicates if this ticket comes from Quentro API (new system) vs local DB (old system)
        /// </summary>
        [JsonIgnore]
        public bool IsQuentro { get; set; } = false;

        /// <summary>
        /// The ticket code (for Quentro tickets that don't have a local TicketId)
        /// </summary>
        [JsonIgnore]
        public string? Code { get; set; }

        /// <summary>
        /// Ticket type/sector name from Quentro API (e.g., "Popular", "VIP", "Sillas 1A")
        /// </summary>
        [JsonIgnore]
        public string? TicketType { get; set; }

        [JsonIgnore]
        public bool Persist => Exists && TicketStatus != TicketStatus.Voided && 
                    TicketStatus != TicketStatus.VoidPending && 
                    TicketStatus != TicketStatus.Invalid;
    }
}
