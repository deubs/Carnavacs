namespace Carnavacs.Api.Domain.Entities
{
    public class EventStats
    {
        public int EventId { get; set; }
        
        public int TotalTickets { get; set; }
        public int UsedTickets { get; set; }
        public int RemainingTickets { get; set; }

        public int TotalGates { get; set; }
        public int OpenGates { get; set; }
        public int ClosedGates { get; set; }

        public int TotalPeople { get; set; }
        public int InsidePeople { get; set; }
        public int OutsidePeople { get; set; }

        public int TotalVehicles { get; set; }
        public int InsideVehicles { get; set; }
        public int OutsideVehicles { get; set; }

        public List<GateInfo> Gates { get; set; } = new List<GateInfo>();
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
