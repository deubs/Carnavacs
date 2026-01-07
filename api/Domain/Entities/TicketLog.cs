namespace Carnavacs.Api.Domain.Entities
{
    /// <summary>
    /// Represents a read entity.
    /// </summary>
    public class TicketLog
    {
        public TicketLog()
        {
            Fecha = DateTime.Now;
        }
        public int Id { get; set; }
        public int? QrEntradaFk { get; set; }
        public DateTime Fecha { get; set; }
        public int EstadoQrFk { get; set; }
        public int AccesoDispositivoFk { get; set; }
        
        /// <summary>
        /// Quentro ticket code (for tickets from Quentro API that don't have a local QrEntradaFk)
        /// </summary>
        public string? QuentroCode { get; set; }
    }
}
