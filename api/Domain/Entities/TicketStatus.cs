using System.Diagnostics.CodeAnalysis;

namespace Carnavacs.Api.Domain.Entities
{
    public enum TicketStatuses { Emmited = 1, OK = 2, VoidPending = 3, Voided = 4, Used = 5, Retry = 6, NotFound = 7 }
    public enum OrderStatuses { OK = 1, InProcess = 2, Refunded = 3 }


    public class TicketStatus
    {
        public virtual TicketStatuses Type { get; private set; }

        public int Id { get { return (int)Type; } }

        public TicketStatus()
        {
        }

        public TicketStatus(TicketStatuses status)
        {
            Type = status;
        }

        public virtual string Name { get { return Type.ToString(); } }


        public static TicketStatus Emmited { get { return new TicketStatus(TicketStatuses.Emmited); } }
        public static TicketStatus OK { get { return new TicketStatus(TicketStatuses.OK); } }
        public static TicketStatus VoidPending { get { return new TicketStatus(TicketStatuses.VoidPending); } }
        public static TicketStatus Voided { get { return new TicketStatus(TicketStatuses.Voided); } }
        public static TicketStatus Used { get { return new TicketStatus(TicketStatuses.Used); } }
        public static TicketStatus Retry { get { return new TicketStatus(TicketStatuses.Retry); } }
        public static TicketStatus NotFound { get { return new TicketStatus(TicketStatuses.NotFound); } }


        public override bool Equals(object? obj)
        {
            return obj is TicketStatus && Type == ((TicketStatus)obj).Type;
        }

        public override int GetHashCode()
        {
            return this.Id;
        }

        public static bool operator ==(TicketStatus e1, TicketStatus e2)
        {
            return Object.ReferenceEquals(e1, e2) || e1.Equals(e2);
        }

        public static bool operator !=(TicketStatus e1, TicketStatus e2)
        {
            return !(e1 == e2);
        }
    }
}
