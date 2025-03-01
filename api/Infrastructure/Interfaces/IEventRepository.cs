using Carnavacs.Api.Domain.Entities;

namespace Carnavacs.Api.Infrastructure.Interfaces
{
    public interface IEventRepository : IRepository<Event>
    {
        Task<Event> GetCurrentAsync();
        Task<EventStats> GetStatsAsync(int? eventId);

        Task<List<Sector>> GetBySectorAsync(int? eventId);
    }
}
