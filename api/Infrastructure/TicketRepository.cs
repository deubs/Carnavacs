using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Domain.Helpers;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;
using System.Net.Sockets;

namespace Carnavacs.Api.Infrastructure
{
    internal class TicketRepository : RepositoryBase, ITicketRepository
    {
        private readonly IQuentroApiClient? _quentroApiClient;

        public TicketRepository(IDbTransaction transaction, IQuentroApiClient? quentroApiClient = null)
            : base(transaction)
        {
            _quentroApiClient = quentroApiClient;
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
                             FROM AccesosEntradasQR e 
                             INNER JOIN Ventas v ON e.VentaFk = v.Id 
                             WHERE EstadoQrFk=@ticketStatus AND V.EstadoVentaFk = @orderStatus AND v.eventofk=@eventId
                             UNION
                             SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId 
                             FROM AccesosUbicacionesQR e 
                             INNER JOIN Ventas v ON e.VentaFk = v.Id 
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
            string query = @"SELECT Id, QRCodigo as Code, EstadoQrFk StatusId FROM AccesosEntradasQR WHERE Id=@Id
                             UNION
                             SELECT Id, QRCodigo as Code, EstadoQrFk StatusId FROM AccesosUbicacionesQR WHERE Id=@Id";
            return await Connection.QuerySingleAsync<Ticket>(query, new { Id = id }, Transaction);
        }

        private async Task<Ticket> GetByCodeAsync(string code)
        {
            string query = @"SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId, VentaFK FROM AccesosEntradasQR e WHERE e.QrCodigo=@code
                             UNION
                             SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId, VentaFK FROM AccesosUbicacionesQR e WHERE e.QrCodigo=@code";
            return await Connection.QueryFirstOrDefaultAsync<Ticket>(query, new { code }, Transaction);
        }

        public Task<string> AddAsync(Ticket entity)
        {
            throw new NotImplementedException();
        }

        public async Task<string> UpdateAsync(Ticket entity)
        {
            string table = entity.GetType() == TicketType.Ubicacion ? "AccesosUbicacionesQR" : "AccesosEntradasQR";
            string upd = $"UPDATE {table} SET EstadoQrFk = @st WHERE Id=@Id;";
            var r = await Connection.ExecuteAsync(upd, new { st = TicketStatus.Used.Id, Id = entity.Id }, Transaction);
            return "ok";
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

        public async Task UseAsync(string code, string deviceId)
        {
            Ticket qr = await this.GetByCodeAsync(code);
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

        public async Task LogQuentroAsync(string code, string? deviceId, TicketStatus status, string? ticketType = null)
        {
            var gateRepo = new GateRepository(Transaction);
            AccessDevice device = await gateRepo.GetDeviceAsync(deviceId ?? "API");

            TicketLog log = new TicketLog
            {
                AccesoDispositivoFk = device.Id,
                EstadoQrFk = status.Id,
                QrEntradaFk = null,
                QuentroCode = code,
                TicketType = ticketType
            };
            await gateRepo.LogEntryAsync(log);
        }

        public async Task<TicketValidationResult> ValidateAsync(string code, bool readOnly = false, string? deviceId = null)
        {
            TicketValidationResult result = new TicketValidationResult();

            var eventRepo = new EventRepository(Transaction);
            var currentEvent = await eventRepo.GetCurrentAsync();

            Ticket qr = await this.GetByCodeAsync(code);

            // If ticket not found locally, try Quentro API
            if (qr == null)
            {
                return await ValidateWithQuentroAsync(code, readOnly, currentEvent, deviceId);
            }

            result.TicketId = qr.Id;

            Venta venta = await Connection.QuerySingleAsync<Venta>("SELECT Id, nombre, eventoFk FROM ventas WHERE id=@ventafk", new { ventafk = qr.VentaFK }, Transaction);
            bool eventoOk = (venta.EventoFk == currentEvent.Id) || qr.Reusable();

            if (qr.Enabled)
            {
                if (eventoOk)
                {
                    result.TicketStatus = TicketStatus.OK;
                    result.M1 = "BIENVENIDO";
                    result.M2 = $"ADELANTE - {venta.Nombre.Truncate(9)}";
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
                result.M2 = $"MULTI {venta.Nombre.Truncate(10)}";
                return result;
            }

            //check quota
            if (qr.Multi)
            {
                int qrType = (int)qr.GetType();
                string qrQuota = "SELECT quota FROM Eventos_TipoEntradas WHERE eventoFk = @evId AND TipoEntradaFk = @qrType";

                int quota = await Connection.QuerySingleAsync<int>(qrQuota, new { evId = venta.EventoFk, qrType }, Transaction);
                string usedCountQuery = "SELECT COUNT(*) FROM QREntradasLecturas WHERE QREntradaFk = @qrId AND Fecha >= @dt";
                int usedCount = await Connection.QuerySingleAsync<int>(usedCountQuery, new { qrId = result.TicketId, dt = currentEvent.Fecha.Date }, Transaction);

                if (usedCount < quota)
                {
                    result.TicketStatus = new TicketStatus(TicketStatuses.OK);
                    result.M1 = $"BIENVENIDO {venta.Nombre.Truncate(9)}";
                    result.M2 = $"RESTAN {quota - usedCount - 1} PASES";
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
            {
                msg += "-" + lastUsed.ToString("HH:mm");
                result.UsedDate = lastUsed.ToString("HH:mm");
            }

            result.M1 = "INVALIDA";
            result.M2 = msg;

            return result;
        }

        /// <summary>
        /// Validate ticket using Quentro API (for tickets from the new system)
        /// </summary>
        /// <param name="code">Ticket code</param>
        /// <param name="readOnly">If true, use /check endpoint; if false, use /validate endpoint</param>
        /// <param name="currentEvent">Current event for date comparison</param>
        /// <param name="deviceId">Device/gate identifier to pass to Quentro API</param>
        private async Task<TicketValidationResult> ValidateWithQuentroAsync(string code, bool readOnly, Event? currentEvent = null, string? deviceId = null)
        {
            var result = new TicketValidationResult
            {
                IsQuentro = true,
                Code = code
            };

            if (_quentroApiClient == null)
            {
                result.TicketStatus = TicketStatus.NotFound;
                result.M1 = "ENTRADA";
                result.M2 = "INVALIDA";
                return result;
            }

            // Get the gate name from the device
            string gateName = "API";
            if (!string.IsNullOrEmpty(deviceId))
            {
                var gateRepo = new GateRepository(Transaction);
                var device = await gateRepo.GetDeviceAsync(deviceId);
                gateName = device.NroSerie ?? deviceId;
            }

            // Use /check for read-only (Verify), /validate to mark as used (Validate)
            var quentroResponse = readOnly
                ? await _quentroApiClient.CheckAsync(code, null, gateName)
                : await _quentroApiClient.ValidateAsync(code, null, gateName);

            if (quentroResponse == null)
            {
                result.TicketStatus = TicketStatus.NotFound;
                result.M1 = "ENTRADA";
                result.M2 = "INVALIDA";
                return result;
            }

            // Capture ticket type/sector from Quentro response
            result.TicketType = quentroResponse.TicketType;

            if (quentroResponse.Valid)
            {
                result.TicketStatus = TicketStatus.OK;
                result.M1 = quentroResponse.M1 ?? "BIENVENIDO";
                result.M2 = quentroResponse.M2 ?? "ADELANTE";
            }
            else
            {
                result.TicketStatus = MapQuentroStatus(quentroResponse.Status ?? quentroResponse.Code);
                result.M1 = quentroResponse.M1 ?? "ENTRADA";

                // Capture usage info from Quentro API response
                if (result.TicketStatus == TicketStatus.Used)
                {
                    result.UsedDate = quentroResponse.UsedDate;
                    result.Gate = quentroResponse.Gate;

                    // If Quentro didn't return usage info, check our local log
                    if (string.IsNullOrEmpty(result.UsedDate))
                    {
                        await PopulateUsageInfoFromLocalLog(result, code, currentEvent);
                    }

                    // Build M2 message similar to old system: "USADA-17:36"
                    string msg = quentroResponse.M2 ?? quentroResponse.Message ?? "USADA";
                    if (!string.IsNullOrEmpty(result.UsedDate) && !msg.Contains(result.UsedDate))
                    {
                        msg += "-" + result.UsedDate;
                    }
                    result.M2 = msg;
                }
                else
                {
                    result.M2 = quentroResponse.M2 ?? quentroResponse.Message ?? "INVALIDA";
                }
            }

            return result;
        }

        /// <summary>
        /// Query the local QREntradasLecturas table for Quentro ticket usage info
        /// </summary>
        private async Task PopulateUsageInfoFromLocalLog(TicketValidationResult result, string code, Event? currentEvent)
        {
            string query = @"SELECT TOP 1 l.Fecha, d.NroSerie as DeviceName
                             FROM QREntradasLecturas l
                             LEFT JOIN AccesosDispositivos d ON l.AccesoDispositivoFk = d.Id
                             WHERE l.QuentroCode = @code
                             ORDER BY l.Fecha";

            var logEntry = await Connection.QueryFirstOrDefaultAsync<(DateTime Fecha, string? DeviceName)>(
                query, new { code }, Transaction);

            if (logEntry.Fecha != default)
            {
                if (currentEvent == null || logEntry.Fecha > currentEvent.Fecha.Date)
                {
                    result.UsedDate = logEntry.Fecha.ToString("HH:mm");
                }
                result.Gate = logEntry.DeviceName;
            }
        }

        /// <summary>
        /// Map Quentro API status string to local TicketStatus
        /// </summary>
        private static TicketStatus MapQuentroStatus(string? status)
        {
            return status?.ToUpperInvariant() switch
            {
                "USED" => TicketStatus.Used,
                "VOIDED" => TicketStatus.Voided,
                "INVALID" => TicketStatus.Invalid,
                "OK" => TicketStatus.OK,
                _ => TicketStatus.NotFound
            };
        }

        public DateTime GetLastSync(string evt)
        {
            string query = "SELECT TOP 1 ISNULL(UPDATEDAT, GETDATE()-10) FROM TicketekTickets ORDER BY id DESC";
            return Connection.ExecuteScalar<DateTime>(query, new { evt }, Transaction);
        }
    }
}
