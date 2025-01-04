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
        public int UsedTickets { get { 
                return TotalTickets - RemainingTickets;
            }
        }
        public int RemainingTickets
        {
            get
            {
                int total = 0;
                foreach (TicketStat stat in TicketStats)
                {
                    if (stat.StatusName == "Habilitado")
                        total += stat.Total;
                }
                return total;
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
        public int PeopleCount { get; set; }
    }
}
