namespace Carnavacs.Api.Domain.Entities
{
    public class Gate
    {
        public int Id { get; set; }
        public string Nombre { get; set; }
        public string Descripcion { get; set; }
        public string SobreNombre { get; set; }
        public bool Enabled { get; set; }
    }
}
