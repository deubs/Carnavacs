using Carnavacs.Api.Domain.Entities;

namespace Carnavacs.Api.Infrastructure.Interfaces
{
    public interface IEventRepository : IRepository<Event>
    {
        Task<Event> GetCurrentAsync();

    }
}
