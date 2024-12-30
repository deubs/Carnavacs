using System.Security.Claims;

namespace Carnavacs.Api.Domain.Entities
{
    public class User
    {
        public int Id { get; internal set; }
        public string UserName { get; internal set; }
        public string Name { get; internal set; }
        public string Email { get; internal set; }
        public IEnumerable<string> Roles { get; internal set; }
    }
}
