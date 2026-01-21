using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using Microsoft.Extensions.Logging;
using System.Data;
using System.Text.RegularExpressions;

namespace Carnavacs.Api.Infrastructure
{
    internal class EventRepository : RepositoryBase, IEventRepository
    {
        public EventRepository(IDbTransaction transaction)
            : base(transaction)
        {
        }

        public async Task<IReadOnlyList<Event>> GetAllAsync()
        {
            var query = "SELECT ev.* FROM Eventos ev INNER JOIN Espectaculos e ON ev.EspectaculoFk=e.id WHERE E.habilitado=@Enabled order by fecha";
            var events = await Connection.QueryAsync<Event>(query, new { Enabled = 1 }, Transaction);
            return events.ToList();
        }

        public async Task<Event> GetByIdAsync(long id)
        {
            var result = await Connection.QuerySingleAsync<Event>("SELECT * FROM [Eventos] (NOLOCK) WHERE [Id] = @Id", new { Id = id }, Transaction);
            return result;
        }

        public async Task<Event> GetCurrentAsync()
        {
            var result = await Connection.QuerySingleAsync<Event>("SELECT TOP 1 * FROM [Eventos] (NOLOCK) WHERE habilitado=1 AND FechaFin>@dt ORDER BY Fecha", new { dt = DateTime.Now }, Transaction);
            return result;
        }

        public async Task<List<Sector>> GetBySectorAsync(int? eventId)
        {
            Event ev = await this.GetEventByIdAsync(eventId);

            // Legacy query for TicketekTickets + Ventas (old system)
            string legacySectorStat = @"SELECT SUBSTRING(section,1,charindex('F',section, 1)-1) Name, count(*) as Total,
                                         sum(case when estadoqrfk in (2,4)  then 0 else 1 end) as Readed
                                         FROM TicketekTickets t
                                         INNER JOIN AccesosEntradasQR qr on convert(varchar, t.barcode) =qr.QRCodigo
                                         INNER JOIN Ventas v on qr.ventaFk=v.id
                                         where status=1 and charindex('F',section, 1)>0 and v.eventofk=@eventFk
                                         group by substring(section,1,charindex('F',section, 1)-1)
                                         union
                                         select 'Popular', count(*), ISNULL(SUM(CASE WHEN estadoqrfk in (2,4) then 0 else 1 end),0) as cant2 from TicketekTickets t
                                         INNER JOIN AccesosEntradasQR qr on convert(varchar, t.barcode) =qr.QRCodigo
                                         INNER JOIN Ventas v on qr.ventaFk=v.id
                                         where status=1 and charindex('F',section, 1)=0 and v.eventofk=@eventFk";

            // Quentro query for new system tickets from QREntradasLecturas
            // EstadoQrFk = 5 means "Ingreso" (successfully entered)
            string quentroSectorStat = @"SELECT
                                    ISNULL(l.TicketType, 'Sin Sector') as Name,
                                    COUNT(*) as Total,
                                    COUNT(*) as Readed
                                  FROM QREntradasLecturas l
                                  WHERE l.QuentroCode IS NOT NULL
                                    AND l.EstadoQrFk = 5
                                    AND CAST(l.Fecha AS DATE) = CAST(@eventDate AS DATE)
                                  GROUP BY l.TicketType";

            // Get legacy results
            var legacyResult = await Connection.QueryAsync<Sector>(legacySectorStat, new { eventFk = ev.Id }, Transaction);

            // Get Quentro results
            var quentroResult = await Connection.QueryAsync<Sector>(quentroSectorStat, new { eventDate = ev.Fecha }, Transaction);

            // Combine both results
            var combinedResult = legacyResult.ToList();
            combinedResult.AddRange(quentroResult);

            return combinedResult.OrderBy(s => s.Name).ToList();
        }

        public Task<string> AddAsync(Event entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> UpdateAsync(Event entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

     
        public async Task<EventStats> GetStatsAsync(int? eventId)
        {
            EventStats stats = new EventStats();
            Event ev = await GetEventByIdAsync(eventId);
            eventId = ev.Id;

            string query = @"SELECT count(*) as Total, EstadoQrFk StatusId, s.Nombre as StatusName 
                                 FROM AccesosEntradasQR e 
                                 INNER JOIN Ventas v ON e.VentaFk = v.Id
                                 INNER JOIN EstadosQR s ON e.EstadoQrFk = s.Id
                                 WHERE V.EstadoVentaFk = @Enabled AND v.eventofk = @EventFk
                                 GROUP BY EstadoQrFk, s.Nombre";
            var r = await Connection.QueryAsync<TicketStat>(query, new { Enabled = 1, EventFk = eventId }, Transaction);

            stats.TicketStats = r.ToList();

            //gates
            string gateQuery = @"SELECT  ad.id DeviceId, ad.NroSerie DeviceName, count(*) PeopleCount, pi.Id GateId, sobrenombre GateNickName
                                FROM QREntradasLecturas qre
                                INNER JOIN AccesosDispositivos ad on qre.AccesoDispositivoFk = ad.Id
                                INNER JOIN puertaingreso pi on pi.id = ad.puertaingresoid 
                                INNER JOIN AccesosEntradasQR e ON qre.QREntradaFk = e.Id
                                INNER JOIN Ventas v ON e.ventaFk = v.id  
                                WHERE qre.EstadoQrFk = 5 AND v.eventofk=@eventFk
                                GROUP BY  pi.Id, ad.id, ad.NroSerie, sobrenombre";

            var r2 = await Connection.QueryAsync<AccessDeviceInfo>(gateQuery, new { Enabled = 1, EventFk = ev.Id }, Transaction);
            foreach (var res in r2)
            {
                var g = stats.Gates.FirstOrDefault(x => x.GateId == res.GateId);
                if (g == null)
                {
                    g = new GateInfo { GateId = res.GateId, GateName = res.GateNickName };
                    stats.Gates.Add(g);
                }
                g.AccessDevices.Add(res);
            }
            return stats;
        }

        private async Task<Event> GetEventByIdAsync(int? eventId)
        {
            Event ev;
            if (!eventId.HasValue)
            {
                ev = await this.GetCurrentAsync();
            }
            else
            {
                ev = await this.GetByIdAsync(eventId.Value);
            }

            return ev;
        }
    }
}