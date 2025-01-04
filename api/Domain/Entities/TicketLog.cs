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
        public int QrEntradaFk { get; set; }
        public DateTime Fecha { get; set; }
        public int EstadoQrFk { get; set; }
        public int AccesoDispositivoFk { get; set; }
    }
}
