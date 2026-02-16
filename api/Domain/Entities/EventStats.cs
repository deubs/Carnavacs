using System.Text.Json.Serialization;

namespace Carnavacs.Api.Domain.Entities
{
    public class EventStats
    {
        public int EventId { get; set; }

        public int TotalTickets => TicketStats.Sum(s => s.Total);

        public int UsedTickets => TicketStats.Where(s => s.StatusId == 5).Sum(s => s.Total);

        public int RemainingTickets => TotalTickets - UsedTickets;

        // Quentro tickets (public sales)
        public int QuentroUsed => TicketStats.Where(s => s.StatusId == 5 && s.Source == "quentro").Sum(s => s.Total);

        // Collaborator tickets (legacy system)
        public int CollaboratorUsed => TicketStats.Where(s => s.StatusId == 5 && s.Source == "collaborator").Sum(s => s.Total);
        public int CollaboratorRemaining => TicketStats.Where(s => s.StatusId == 2 && s.Source == "collaborator").Sum(s => s.Total);

        public int TotalGates { get; set; }
        public int OpenGates { get; set; }
        public int ClosedGates { get; set; }

        public List<GateInfo> Gates { get; set; } = new List<GateInfo>();

        [JsonIgnore]
        public List<TicketStat> TicketStats { get; set; } = new List<TicketStat>();
    }

    public class TicketStat
    {
        public int Total { get; set; }
        public int StatusId { get; set; }
        public string StatusName { get; set; }
        public string Source { get; set; }
    }

    public class GateInfo
    {
        public int GateId { get; set; }
        public string GateName { get; set; }
        public List<AccessDeviceInfo> AccessDevices { get; set; } = new List<AccessDeviceInfo>();
    }

    public class AccessDeviceInfo
    {
        public int DeviceId { get; set; }
        public string DeviceName { get; set; }
        public string? FriendlyName { get; set; }
        public int PeopleCount { get; set; }

        [JsonIgnore]
        public int GateId { get; set; }

        [JsonIgnore]
        public string GateNickName { get; set; }
    }
}
