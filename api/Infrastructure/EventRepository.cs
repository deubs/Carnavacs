﻿using Carnavacs.Api.Domain.Entities;
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
            var query = "SELECT * FROM Eventos WHERE habilitado=@Enabled order by fecha";
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

     
        public async Task<EventStats> GetStatsAsync()
        {
            EventStats stats = new EventStats();
            var ev = await this.GetCurrentAsync();
            string query = @"SELECT count(*) as Total, EstadoQrFk StatusId, s.Nombre as StatusName 
                                 FROM AccesosEntradasQR e INNER JOIN Ventas v ON e.VentaFk = v.Id
                                    INNER JOIN EstadosQR s ON e.EstadoQrFk = s.Id
                                 WHERE V.EstadoVentaFk = @Enabled AND v.eventofk = @EventFk
                                 GROUP BY EstadoQrFk, s.Nombre";
            var r = await Connection.QueryAsync<TicketStat>(query, new { Enabled = 1, EventFk = ev.Id }, Transaction);

            stats.TicketStats = r.ToList();

            //gates
            string gateQuery = @"select ad.NroSerie,sobrenombre, count(*) from QREntradasLecturas qre
                                 inner join AccesosDispositivos ad on qre.AccesoDispositivoFk = ad.Id
                                 inner join puertaingreso pi on pi.id = ad.puertaingresoid 
                                 where fecha > '2023-02-25 12:00'
                                 group by ad.NroSerie, sobrenombre order by ad.NroSerie";

            var r2 = await Connection.QueryAsync<TicketStat>(query, new { Enabled = 1, EventFk = ev.Id }, Transaction);


            return stats;
        }
    }
}