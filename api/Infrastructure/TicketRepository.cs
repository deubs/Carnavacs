using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Dapper;
using System.Data;

namespace Carnavacs.Api.Infrastructure
{
    internal class TicketRepository : RepositoryBase, ITicketRepository
    {
        public TicketRepository(IDbTransaction transaction)
            : base(transaction)
        {
        }

        /// <summary>
        /// Get All Enabled tickets
        /// </summary>
        /// <returns></returns>
        public async Task<IReadOnlyList<Ticket>> GetAllAsync()
        {
            var eventRepo = new EventRepository(Transaction);
            var currentEvent = await eventRepo.GetCurrentAsync();
            if (currentEvent == null)
                return new List<Ticket>();

            string query = @"SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId 
                             FROM AccesosEntradasQR e INNER JOIN Ventas v ON e.VentaFk = v.Id 
                             WHERE EstadoQrFk=@ticketStatus AND V.EstadoVentaFk = @orderStatus AND v.eventofk=@eventId";

            var tickets = await Connection.QueryAsync<Ticket>(query, new
            {
                ticketStatus = TicketStatus.OK.Id,
                orderStatus = (int)OrderStatuses.OK,
                eventId = currentEvent.Id
            }, Transaction);
            return tickets.ToList();
        }

        public async Task<Ticket> GetByIdAsync(long id)
        {
            string query = "SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId FROM AccesosEntradasQR WHERE Id=@Id";
            return await Connection.QuerySingleAsync<Ticket>(query, new { Id = id }, Transaction);
        }

      
        public Task<string> AddAsync(Ticket entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> UpdateAsync(Ticket entity)
        {
            throw new NotImplementedException();
        }

        public Task<string> DeleteAsync(long id)
        {
            throw new NotImplementedException();
        }

        public Task UseAsync(int ticketId, string? device)
        {
            throw new NotImplementedException();
        }

        public async Task<TicketValidationResult> ValidateAsync(string code)
        {
            TicketValidationResult result = new TicketValidationResult();

            string query = @"SELECT e.Id, QRCodigo as Code, EstadoQrFk StatusId 
                             FROM AccesosEntradasQR e INNER JOIN Ventas v ON e.VentaFk = v.Id 
                             WHERE e.QrCodigo=@code";

            var ticket = await Connection.QueryFirstOrDefaultAsync<Ticket>(query, new {code}, Transaction);

            if (ticket == null)
            {
                result.TicketStatus = TicketStatus.NotFound;
            }
            else
            {
                result.TicketStatus = new TicketStatus((TicketStatuses)ticket.StatusId);
            }
            return result;
        }
    }
}