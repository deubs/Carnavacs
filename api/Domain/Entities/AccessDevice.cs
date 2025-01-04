namespace Carnavacs.Api.Domain.Entities
{
    public class AccessDevice
    {
        public int Id { get; set; }
        public  string NroSerie{ get; set; }
        public int AccesoSectorFk { get; set; }
        public int PuertaIngresoId { get; set; }
        
    }
}
