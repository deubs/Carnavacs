using System.Diagnostics;
using System.IO;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure;
using Dapper;
using Microsoft.AspNetCore.Mvc;

namespace Carnavacs.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HealthController : ControllerBase
    {
        private static readonly DateTime _startTime = DateTime.UtcNow;
        private readonly DapperContext _dbContext;
        private readonly ILogger<HealthController> _logger;

        public HealthController(DapperContext dbContext, ILogger<HealthController> logger)
        {
            _dbContext = dbContext;
            _logger = logger;
        }

        [HttpGet]
        [EndpointName("Health")]
        [EndpointSummary("Health check with system metrics")]
        public async Task<ApiResponse<HealthReport>> Get()
        {
            var report = new HealthReport
            {
                Timestamp = DateTime.UtcNow.ToString("o"),
                UptimeSeconds = (long)(DateTime.UtcNow - _startTime).TotalSeconds,
                System = GetSystemInfo(),
                Database = await CheckDatabaseAsync()
            };

            report.Status = report.Database.Connected ? "healthy" : "degraded";

            return new ApiResponse<HealthReport>
            {
                Success = true,
                Result = report
            };
        }

        private SystemInfo GetSystemInfo()
        {
            var process = Process.GetCurrentProcess();

            // CPU: sample over ~100ms
            var startCpu = process.TotalProcessorTime;
            var startTime = DateTime.UtcNow;
            Thread.Sleep(100);
            process.Refresh();
            var endCpu = process.TotalProcessorTime;
            var endTime = DateTime.UtcNow;
            var cpuPercent = (endCpu - startCpu).TotalMilliseconds /
                            (endTime - startTime).TotalMilliseconds /
                            Environment.ProcessorCount * 100;

            // Memory
            var memUsedMb = process.WorkingSet64 / (1024 * 1024);
            var gcInfo = GC.GetGCMemoryInfo();
            var totalMemMb = gcInfo.TotalAvailableMemoryBytes / (1024 * 1024);
            var memPercent = totalMemMb > 0 ? (double)memUsedMb / totalMemMb * 100 : 0;

            // Disk
            var appPath = AppContext.BaseDirectory;
            var driveRoot = Path.GetPathRoot(appPath) ?? "C:\\";
            var drive = new DriveInfo(driveRoot);
            var diskPercent = 100.0 - ((double)drive.AvailableFreeSpace / drive.TotalSize * 100);
            var diskFreeMb = drive.AvailableFreeSpace / (1024 * 1024);

            return new SystemInfo
            {
                CpuPercent = Math.Round(cpuPercent, 1),
                MemoryPercent = Math.Round(memPercent, 1),
                MemoryUsedMb = memUsedMb,
                MemoryTotalMb = totalMemMb,
                DiskPercent = Math.Round(diskPercent, 1),
                DiskFreeMb = diskFreeMb,
                MachineName = Environment.MachineName
            };
        }

        private async Task<DatabaseInfo> CheckDatabaseAsync()
        {
            var sw = Stopwatch.StartNew();
            try
            {
                using var conn = _dbContext.CreateConnection();
                conn.Open();
                await conn.QuerySingleAsync<int>("SELECT 1");
                sw.Stop();
                return new DatabaseInfo { Connected = true, ResponseTimeMs = (int)sw.ElapsedMilliseconds };
            }
            catch (Exception ex)
            {
                sw.Stop();
                _logger.LogWarning(ex, "Database health check failed");
                return new DatabaseInfo { Connected = false, ResponseTimeMs = (int)sw.ElapsedMilliseconds };
            }
        }
    }
}
