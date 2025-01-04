
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

    }
}
