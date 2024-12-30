using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Infrastructure;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Localization;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Resources;
using System.Text;

namespace Carnavacs.Api.Controllers
{
    [Produces("application/json")]
    [Route("[controller]")]
    [ApiExplorerSettings(IgnoreApi = true)]

    public class AuthController : BaseApiController
    {
        private readonly LoginManager _loginManager;

        public AuthController(LoginManager loginManager)
        {
            _loginManager = loginManager;
        }

        [HttpGet]
        public IActionResult NotAuthorized()
        {
            return Unauthorized();
        }
    
        /// <summary>
        /// User Login. Returns complete User Model with roles or metadata that specifies a 2fa method is required if .  
        /// </summary>
        /// <param name="login">LoginModel with username and password</param>
        /// <returns></returns>
        [HttpPost]
        [ProducesResponseType<ApiResponse<Domain.Entities.User>>(StatusCodes.Status200OK)]
        [ProducesErrorResponseType(typeof(BadRequest))]
        [AllowAnonymous]
        public async Task<IActionResult> Login([FromBody] LoginModel login)
        {
            ApiResponse<Domain.Entities.User> response = new ApiResponse<Domain.Entities.User>();
            try
            {
                response.Result = _loginManager.Login(login);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost("Logout")]
        public async Task<IActionResult> Logout(string access_token)
        {
            return Ok(null);
        }

    }
}
