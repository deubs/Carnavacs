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
                return t == TicketType.Comision;
            }
        }

        public virtual bool Master => this.GetType() == TicketType.Master;

        public virtual bool Reusable()
        {
            TicketType t = GetType();
            return this.Master || t == TicketType.Colaborador || t == TicketType.Comision;
        }

        public virtual TicketType GetType()
        {
            int sys = 0;
            Int32.TryParse(Code.Substring(0, 2), out sys);
            if (sys == 10)
            {
                Int32.TryParse(Code.Substring(2, 2), out sys);
                return (TicketType)sys;
            }
            if (sys > 41) 
                return TicketType.Ubicacion;

            return TicketType.Desconocido;


        }

    }
}
