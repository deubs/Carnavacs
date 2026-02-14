using Carnavacs.Api.Domain.Entities;

namespace Carnavacs.Api.Infrastructure.Interfaces
{
    public interface IUserRepository : IRepository<User>
    {
        Task<User> GetByUsernameAsync(string username);
        Task<IEnumerable<string>> GetRolesByUserIdAsync(int userId);
    }
}
