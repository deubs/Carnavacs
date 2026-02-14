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

        public async Task<User> GetByUsernameAsync(string username)
        {
            var sql = @"SELECT [Id], [Username] AS UserName, [FirstName] + ' ' + [LastName] AS Name,
                         [Email], [Password]
                         FROM [Usuarios] (NOLOCK)
                         WHERE [Username] = @Username";
            var result = await Connection.QuerySingleOrDefaultAsync<User>(sql, new { Username = username }, Transaction);
            return result;
        }

        public async Task<IEnumerable<string>> GetRolesByUserIdAsync(int userId)
        {
            var sql = @"SELECT r.[Nombre]
                         FROM [Usuarios_Roles] ur
                         JOIN [Roles] r ON ur.[RoleFk] = r.[Id]
                         WHERE ur.[UserFk] = @UserId";
            var result = await Connection.QueryAsync<string>(sql, new { UserId = userId }, Transaction);
            return result;
        }

        public Task<IReadOnlyList<User>> GetAllAsync()
        {
            throw new NotImplementedException();
        }
    }
}
