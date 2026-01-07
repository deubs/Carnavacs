using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.Data.SqlClient;
using System.Data;
using System.Data.Common;

namespace Carnavacs.Api.Infrastructure
{
    public class UnitOfWork : IUnitOfWork
    {
        public IEventRepository _eventRepository;
        public IGateRepository _gateRepository;
        public ITicketRepository _ticketRepository;

        private IDbConnection _connection;
        private IDbTransaction _transaction;
        private bool _disposed;
        private readonly IQuentroApiClient? _quentroApiClient;

        public UnitOfWork(DapperContext context, IQuentroApiClient? quentroApiClient = null)
        {
            _connection = context.CreateConnection();
            _connection.Open();
            _transaction = _connection.BeginTransaction();
            _quentroApiClient = quentroApiClient;
        }

        public IEventRepository Events => _eventRepository ?? (_eventRepository = new EventRepository(_transaction));
   
        public IGateRepository Gates => _gateRepository ?? (_gateRepository = new GateRepository(_transaction));

        public ITicketRepository Tickets => _ticketRepository ?? (_ticketRepository = new TicketRepository(_transaction, _quentroApiClient));

        public void Commit()
        {
            try
            {
                _transaction.Commit();
            }
            catch
            {
                _transaction.Rollback();
                throw;
            }
            finally
            {
                _transaction.Dispose();
                _transaction = _connection.BeginTransaction();
                resetRepositories();
            }
        }

        private void resetRepositories()
        {
            _eventRepository = null;
            _gateRepository = null;
            _ticketRepository = null;
        }

        public void Dispose()
        {
            dispose(true);
            GC.SuppressFinalize(this);
        }

        private void dispose(bool disposing)
        {
            if (!_disposed)
            {
                if (disposing)
                {
                    if (_transaction != null)
                    {
                        _transaction.Dispose();
                        _transaction = null;
                    }
                    if (_connection != null)
                    {
                        _connection.Dispose();
                        _connection = null;
                    }
                }
                _disposed = true;
            }
        }

        ~UnitOfWork()
        {
            dispose(false);
        }
    }
}
