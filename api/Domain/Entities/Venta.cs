namespace Carnavacs.Api.Domain.Entities
{
    public class Venta
    {
        public string _nombre { get; set; }
        public int Id { get; set; }

        public int EventoFk { get; set; }
        public string Nombre { 
            get
            {
                return _nombre.ToUpper();
            }
            set
            {
                _nombre = value;
            }
        }

    }
}
