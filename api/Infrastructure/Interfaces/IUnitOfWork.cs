namespace Carnavacs.Api.Infrastructure.Interfaces
{
    public interface IUnitOfWork : IDisposable
    {
        IEventRepository Events { get; }

        IGateRepository Gates { get; }

        ITicketRepository Tickets { get; }


        void Commit();

    }
}
