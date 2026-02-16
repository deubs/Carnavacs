using System.Text.Json.Serialization;

namespace Carnavacs.Api.Domain.Entities
{
    public class EventStats
    {
        public int EventId { get; set; }

        public int TotalTickets
        {
            get
            {
                int total = 0;
                foreach (TicketStat stat in TicketStats)
                {
                    total += stat.Total;
                }
                return total;
            }
        }
        public int UsedTickets
        {
            get
            {
                int total = 0;
                foreach (TicketStat stat in TicketStats)
                {
                    if (stat.StatusId == 5)
                        total += stat.Total;
                }
                return total;
            }
        }
        public int RemainingTickets
        {
            get
            {
                return TotalTickets - UsedTickets;
            }
        }

        public int TotalGates { get; set; }
        public int OpenGates { get; set; }
        public int ClosedGates { get; set; }

        public List<GateInfo> Gates { get; set; } = new List<GateInfo>();

        public List<TicketStat> TicketStats { get; set; } = new List<TicketStat>();
    }

    public class TicketStat
    {
        public int Total { get; set; }
        public int StatusId { get; set; }
        public string StatusName { get; set; }
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
