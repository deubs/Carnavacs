﻿namespace Carnavacs.Api.Domain.Entities
{
    public class Event
    {
        public int Id { get; set; }
        public DateTime Fecha { get; set; }
        public string Nombre { get; set; }
        public  bool Habilitado { get; set; }
    }
}
