using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;

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
            var events = await Connection.QueryAsync<Event>(query, new {Enabled = 1}, Transaction);
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

    }
}