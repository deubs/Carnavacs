namespace Carnavacs.Api.Domain.Entities
{
    /// <summary>
    /// Represents a ticket entity.
    /// </summary>
    public class Ticket
    {
        public int Id { get; set; }
        public int StatusId { get; set; }
        public required string Code { get; set; }

        public int VentaFK { get; set; }

        public bool Enabled => StatusId == TicketStatus.OK.Id || this.StatusId == TicketStatus.Emmited.Id;

        public bool Void => StatusId == TicketStatus.VoidPending.Id || StatusId == TicketStatus.Voided.Id;

        public bool Multi
        {
            get
            {
                TicketType t = GetType();
                return t == TicketType.Acceso || t == TicketType.Comision;
            }
        }

        public virtual bool Master => this.GetType() == TicketType.Master;

        public virtual bool Reusable()
        {
            TicketType t = GetType();
            return this.Master || t == TicketType.Colaborador || t == TicketType.Acceso || t==TicketType.Comision;
        }

        public virtual TicketType GetType()
        {
            int tipo = 0;
            string id = Code.Substring(2, 2);
            Int32.TryParse(id, out tipo);
            return (TicketType)tipo;
        }

    }
}
