using System.ComponentModel;

namespace Carnavacs.Api
{
    public enum TicketType
    {
        Desconocido = 0,
        [Description("General")]
        General = 1,
        [Description("Menor")]
        Menor = 2,
        [Description("Silla Extra VIP")]
        SillaExtraVIP = 3,
        [Description("Silla Extra")]
        SillaExtra = 4,
        [Description("Clarin")]
        Clarin = 5,
        [Description("Mega Fiesta")]
        MegafiestaVip = 6,
        [Description("Liberado")]
        Liberados = 7,
        PromocionFlecha = 8,
        [Description("Estacionamiento")]
        Estacionamiento = 9,
        [Description("Gualeguaychu")]
        Gualeguaychu = 10,
        [Description("Clarin 2x1")]
        Clarin2x1 = 11,
        [Description("Combi")]
        Combi = 12,
        [Description("Bus")]
        Buses = 13,
        [Description("Promo Uno")]
        PromoUno = 14,
        [Description("Anticipada")]
        Anticipada = 15,
        [Description("Mayor")]
        Mayores = 16,
        [Description("General Cap")]
        GeneralCap = 17,
        [Description("General Entre Rios")]
        GeneralEntreRios = 20,
        [Description("SADOP")]
        SADOP = 21,
        [Description("Popular")]
        Popular = 22,
        [Description("Fiesta de la Reina")]
        Reina = 23,
        [Description("Invitado")]
        Invitado = 24,
        [Description("Cotillon")]
        Cotillon = 26,
        [Description("Municipalidad")]
        Municipalidad = 27,
        [Description("General Club")]
        GeneralClub = 28,
        [Description("Cantina")]
        Cantina = 29,
        [Description("Prensa")]
        Prensa = 30,
        [Description("Colaborador")]
        Colaborador = 31,
        [Description("Libre Acceso")]
        Master = 32,
        [Description("Acceso")]
        Acceso = 33,
        [Description("Comision")]
        Comision = 34,
        [Description("Ubicacion")]
        Ubicacion = 99
    }

}