using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;

namespace Carnavacs.Api.Infrastructure
{
    internal class GateRepository : RepositoryBase, IGateRepository
    {
        public GateRepository(IDbTransaction transaction)
            : base(transaction)
        {
        }

        /// <summary>
        /// Get All Enabled gates
        /// </summary>
        /// <returns></returns>
        public async Task<IReadOnlyList<Gate>> GetAllAsync()
        {
            var eventRepo = new EventRepository(Transaction);
            var currentEvent = await eventRepo.GetCurrentAsync();
            if (currentEvent == null)
                return new List<Gate>();

            string query = @"SELECT * FROM [PuertaIngreso] WHERE Enabled=@enabled";

            var gates = await Connection.QueryAsync<Gate>(query, new { enabled = 1 }, Transaction);
            return gates.ToList();
        }

        public async Task<IReadOnlyList<AccessDevice>> GetAllDevicesAsync()
        {

            string query = @"select DISTINCT ad.* from [dbo].[AccesosDispositivos] ad INNER JOIN QREntradasLecturas l  ON l.AccesoDispositivoFk = ad.Id
                             WHERE l.QREntradaFk>=414647 and PuertaIngresoId is not null order by ad.nroserie";

            var devices = await Connection.QueryAsync<AccessDevice>(query,null, Transaction);
            return devices.ToList();
        }

        public async Task<Gate> GetByIdAsync(long id)
        {
            string query = "SELECT * FROM [PuertaIngreso] WHERE Id=@Id";
            return await Connection.QuerySingleAsync<Gate>(query, new { Id = id }, Transaction);
        }

      
        public Task<string> AddAsync(Gate entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> UpdateAsync(Gate entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

        public Task UseAsync(int gateId, string? device)
        {
            throw new NotImplementedException();
        }

        internal async Task<AccessDevice> GetDeviceAsync(string deviceId)
        {
            string query = "SELECT * FROM [AccesosDispositivos] WHERE NroSerie=@deviceId";
            AccessDevice device = await Connection.QuerySingleOrDefaultAsync<AccessDevice>(query, new { deviceId }, Transaction);
            
            if (device == null)
            {
                device = new AccessDevice
                {
                    AccesoSectorFk = 1,
                    NroSerie = deviceId
                };
                device.Id = await this.AddDeviceAsync(device);
            }
            return device;

        }

        private async Task<int> AddDeviceAsync(AccessDevice device)
        {
            string insertQuery = @"INSERT INTO dbo.[AccesosDispositivos](NroSerie, AccesoSectorFk)
                        OUTPUT INSERTED.[Id]
                        VALUES(@deviceId, @accesoSectorFk);";
            return await Connection.QuerySingleAsync<int>(insertQuery, new {deviceId=device.NroSerie, accesoSectorFk= device.AccesoSectorFk}, Transaction);
        }

        internal async Task<int> LogEntryAsync(TicketLog log)
        {

            string insertQuery = @"INSERT INTO dbo.[QREntradasLecturas] (QrEntradaFk, Fecha, EstadoQrFk, AccesoDispositivoFk, QuentroCode)
                        OUTPUT INSERTED.[Id]
                        VALUES(@qrId, @dt, @ticketStatusId, @deviceId, @quentroCode);";
            return await Connection.QuerySingleAsync<int>(insertQuery, new { 
                qrId = log.QrEntradaFk,
                dt = log.Fecha,
                ticketStatusId = log.EstadoQrFk,
                deviceId = log.AccesoDispositivoFk,
                quentroCode = log.QuentroCode}, Transaction);

        }
    }
}