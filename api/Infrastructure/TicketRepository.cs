using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;
using System.Net.Sockets;

namespace Carnavacs.Api.Infrastructure
{
    internal class TicketRepository : RepositoryBase, ITicketRepository
    {
        public TicketRepository(IDbTransaction transaction)
            : base(transaction)
        {
        }

        /// <summary>
        /// Get All Enabled tickets
        /// </summary>
        /// <returns></returns>
        public async Task<IReadOnlyList<Ticket>> GetAllAsync()
        {
            var eventRepo = new EventRepository(Transaction);
            var currentEvent = await eventRepo.GetCurrentAsync();
            if (currentEvent == null)
                return new List<Ticket>();

            string query = @"SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId 
                             FROM AccesosEntradasQR e INNER JOIN Ventas v ON e.VentaFk = v.Id 
                             WHERE EstadoQrFk=@ticketStatus AND V.EstadoVentaFk = @orderStatus AND v.eventofk=@eventId";

            var tickets = await Connection.QueryAsync<Ticket>(query, new
            {
                ticketStatus = TicketStatus.OK.Id,
                orderStatus = (int)OrderStatuses.OK,
                eventId = currentEvent.Id
            }, Transaction);
            return tickets.ToList();
        }

        public async Task<Ticket> GetByIdAsync(long id)
        {
            string query = "SELECT Id, QRCodigo as Code, EstadoQrFk StatusId FROM AccesosEntradasQR WHERE Id=@Id";
            return await Connection.QuerySingleAsync<Ticket>(query, new { Id = id }, Transaction);
        }

        private async Task<Ticket> GetByCodeAsync(string code)
        {
            string query = @"SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId, VentaFK FROM AccesosEntradasQR e WHERE e.QrCodigo=@code";
            return await Connection.QueryFirstOrDefaultAsync<Ticket>(query, new { code }, Transaction);
        }

        public Task<string> AddAsync(Ticket entity)
        {
            throw new NotImplementedException();
        }

        public async Task<string> UpdateAsync(Ticket entity)
        {
            string upd = "UPDATE AccesosEntradasQR SET EstadoQrFk = @st WHERE Id=@Id;";
            var r = await Connection.ExecuteAsync(upd, new { st = TicketStatus.Used.Id, Id = entity.Id }, Transaction);
            return "ok";
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

        public async Task UseAsync(int ticketId, string deviceId)
        {
            Ticket qr = await this.GetByIdAsync(ticketId);
            bool enabled = qr.Enabled;
            if (qr.Enabled)
                await this.UpdateAsync(qr);

            var gateRepo = new GateRepository(Transaction);
            AccessDevice device = await gateRepo.GetDeviceAsync(deviceId);

            TicketLog log = new TicketLog
            {
                AccesoDispositivoFk = device.Id,
                EstadoQrFk = enabled ? TicketStatus.Used.Id : TicketStatus.Retry.Id,
                QrEntradaFk = qr.Id
            };
            await gateRepo.LogEntryAsync(log);

        }

        public async Task<TicketValidationResult> ValidateAsync(string code)
        {
            TicketValidationResult result = new TicketValidationResult();

            var eventRepo = new EventRepository(Transaction);
            var currentEvent = await eventRepo.GetCurrentAsync();


            Ticket qr = await this.GetByCodeAsync(code);

            if (qr == null)
            {
                result.TicketStatus = TicketStatus.NotFound;
                result.M1 = "ENTRADA";
                result.M2 = "INVALIDA";
                return result;
            }

            result.TicketId = qr.Id;

            int evId = await Connection.QuerySingleAsync<int>("SELECT eventoFk FROM ventas WHERE id=@ventafk", new { ventafk = qr.VentaFK }, Transaction);
            bool eventoOk = (evId == currentEvent.Id) || qr.Reusable();


            if (qr.Enabled)
            {
                if (eventoOk)
                {
                    result.TicketStatus = TicketStatus.OK;
                    result.M1 = "BIENVENIDO";
                    result.M2 = "ADELANTE";
                }
                else
                {
                    result.TicketStatus = TicketStatus.Invalid;
                    result.M1 = "ENTRADA INVALIDA";
                    result.M2 = "OTRA NOCHE";
                }
                return result;
            }

            if (qr.Master)
            {
                result.TicketStatus = new TicketStatus(TicketStatuses.OK);
                result.M1 = "BIENVENIDO";
                result.M2 = "ADELANTE MAESTRO";
                return result;
            }

            //check quota
            if (qr.Multi)
            {
                int qrType = (int)qr.GetType();
                string qrQuota = "SELECT quota FROM Eventos_TipoEntradas WHERE eventoFk = @evId AND TipoEntradaFk = @qrType";
                int quota = await Connection.QuerySingleAsync<int>(qrQuota, new { evId, qrType }, Transaction);
                string usedCountQuery = "SELECT COUNT(*) FROM QREntradasLecturas WHERE QREntradaFk = @qrId AND Fecha >= @dt";
                int usedCount = await Connection.QuerySingleAsync<int>(usedCountQuery, new { qrId = result.TicketId, dt = currentEvent.Fecha.Date }, Transaction);

                if (usedCount < quota)
                {
                    result.TicketStatus = new TicketStatus(TicketStatuses.OK);
                    result.M1 = "BIENVENIDO";
                    result.M2 = $"RESTAN {quota - usedCount-1} PASES";
                    return result;
                }
            }

            if (qr.Void)
            {
                result.TicketStatus = new TicketStatus(TicketStatuses.Voided);
                result.M1 = "ENTRADA";
                result.M2 = "ANULADA";
                return result;
            }

            result.TicketStatus = new TicketStatus(TicketStatuses.Used);
            string msg = "USADA";
            string lastUsedQuery = "SELECT TOP 1 fecha FROM QREntradasLecturas WHERE QREntradaFk = @qrId ORDER BY FECHA";
            DateTime lastUsed = await Connection.QuerySingleOrDefaultAsync<DateTime>(lastUsedQuery, new { qrId = result.TicketId }, Transaction);
            if (lastUsed > currentEvent.Fecha.Date)
                msg += "-" + lastUsed.ToString("HH:mm");

            result.M1 = "INVALIDA";
            result.M2 = msg;

            return result;
        }

        public DateTime GetLastSync(string evt)
        {

            string query = "SELECT ISNULL(MAX(UPDATEDAT), GETDATE()-365) FROM TicketekTickets WHERE showname=@evt";
            return Connection.ExecuteScalar<DateTime>(query, new {evt}, Transaction);
        }
    }
}