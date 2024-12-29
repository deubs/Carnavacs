namespace Carnavacs.Api.Domain.Entities
{
    public class Ticket
    {
        public int Id { get; set; }
        public  bool Enabled => StatusId == TicketStatus.OK.Id;

        public int StatusId { get; set; }

        public required string Code { get; set; }
    }
}
