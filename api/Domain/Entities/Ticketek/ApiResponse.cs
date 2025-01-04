namespace Carnavacs.Api.Domain.Entities.Ticketek
{
    public class ApiResponse
    {
        public List<Ticket> Tickets { get; set; }
        public int RemainingTickets { get; set; }
        public int RemainingPages { get; set; }
        public int PageLength { get; set; }
        public string LastId { get; set; }
        public string? SelectedId { get; set; }

    }

    public class Ticket
    {
        public string _id { get; set; }
        public string Event { get; set; }
        public int Sequence { get; set; }
        public long Barcode { get; set; }
        public DateTime CreatedAt { get; set; }
        public string Dlvy_type { get; set; }
        public int Mjt { get; set; }
        public string Price_type { get; set; }
        public string Row { get; set; }
        public int Seat { get; set; }
        public string Section { get; set; }
        public string Showname { get; set; }
        public int Status { get; set; }
        public DateTime UpdatedAt { get; set; }
    }
}
