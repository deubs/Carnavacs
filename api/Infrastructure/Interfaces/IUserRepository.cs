using Carnavacs.Api.Domain.Entities;

namespace Carnavacs.Api.Infrastructure.Interfaces
{
    public interface IUserRepository : IRepository<User>
    {
        Task<User> GetByUsernameAndPasswordAsync(string username, string password);
    }
}
