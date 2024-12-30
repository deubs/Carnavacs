using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;

namespace Carnavacs.Api.Infrastructure
{
    internal class UserRepository : RepositoryBase, IUserRepository
    {
        public UserRepository(IDbTransaction transaction)
            : base(transaction)
        {
        }

        public async Task<User> GetByIdAsync(long id)
        {
            var result = await Connection.QuerySingleAsync<User>("SELECT * FROM [Usuarios] (NOLOCK) WHERE [Id] = @Id", new { Id = id }, Transaction);
            return result;
        }

        public Task<string> AddAsync(User entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> UpdateAsync(User entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

        public async Task<User> GetByUsernameAndPasswordAsync(string username, string password)
        {
            var result = await Connection.QuerySingleOrDefaultAsync<User>("SELECT * FROM [Usuarios] (NOLOCK) WHERE [Id] = @Id", new { Username = username }, Transaction);
            return result;
        }

        public Task<IReadOnlyList<User>> GetAllAsync()
        {
            throw new NotImplementedException();
        }
    }
}