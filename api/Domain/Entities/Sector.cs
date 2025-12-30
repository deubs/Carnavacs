namespace Carnavacs.Api.Domain.Entities
{
    /// <summary>
    /// Represents a sector of corsodromo with details about occupation and entered count.
    /// </summary>
    public class Sector
    {
        /// <summary>
        /// Gets or sets the unique identifier for the sector.
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Gets or sets friendly name of the sector.
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Gets or sets the total count of tickets sold for the sector.
        /// </summary>
        public string Total { get; set; }

        /// <summary>
        /// Gets or sets the count of tickets ingresed for the sector.
        /// </summary>
        public string Readed { get; set; }
    }
}
