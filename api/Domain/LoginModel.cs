
namespace Carnavacs.Api.Domain
{
    /// <summary>
    /// Represents the login model containing username and password.
    /// </summary>
    public class LoginModel
    {
        /// <summary>
        /// Email like username. 
        /// </summary>
        public string Username { get; set; } = string.Empty;

        /// <summary>
        /// User's password.
        /// </summary>
        public string Password { get; set; } = string.Empty;
    }
}
