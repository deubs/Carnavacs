using System.Security.Claims;
using System.Text.Json.Serialization;

namespace Carnavacs.Api.Domain.Entities
{
    public class User
    {
        public int Id { get; internal set; }
        public string UserName { get; internal set; }
        public string Name { get; internal set; }
        public string Email { get; internal set; }
        [JsonIgnore]
        public string Password { get; internal set; }
        public IEnumerable<string> Roles { get; internal set; }
    }
}
