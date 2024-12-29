using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;

namespace Carnavacs.Api.Infrastructure
{
    internal class GateRepository : RepositoryBase, IGateRepository
    {
        public GateRepository(IDbTransaction transaction)
            : base(transaction)
        {
        }

        /// <summary>
        /// Get All Enabled gates
        /// </summary>
        /// <returns></returns>
        public async Task<IReadOnlyList<Gate>> GetAllAsync()
        {
            var eventRepo = new EventRepository(Transaction);
            var currentEvent = await eventRepo.GetCurrentAsync();
            if (currentEvent == null)
                return new List<Gate>();

            string query = @"SELECT * FROM [PuertaIngreso] WHERE Enabled=@enabled";

            var gates = await Connection.QueryAsync<Gate>(query, new { enabled = 1 }, Transaction);
            return gates.ToList();
        }

        public async Task<Gate> GetByIdAsync(long id)
        {
            string query = "SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId FROM AccesosEntradasQR WHERE Id=@Id";
            return await Connection.QuerySingleAsync<Gate>(query, new { Id = id }, Transaction);
        }

      
        public Task<string> AddAsync(Gate entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> UpdateAsync(Gate entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

        public Task UseAsync(int gateId, string? device)
        {
            throw new NotImplementedException();
        }
    }
}