namespace Carnavacs.Api.Domain.Entities
{
    public class HealthReport
    {
        public string Status { get; set; }
        public long UptimeSeconds { get; set; }
        public string Timestamp { get; set; }
        public SystemInfo System { get; set; }
        public DatabaseInfo Database { get; set; }
    }

    public class SystemInfo
    {
        public double CpuPercent { get; set; }
        public double MemoryPercent { get; set; }
        public long MemoryUsedMb { get; set; }
        public long MemoryTotalMb { get; set; }
        public double DiskPercent { get; set; }
        public long DiskFreeMb { get; set; }
        public string MachineName { get; set; }
    }

    public class DatabaseInfo
    {
        public bool Connected { get; set; }
        public int ResponseTimeMs { get; set; }
    }
}
