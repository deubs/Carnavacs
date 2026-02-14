using Carnavacs.Api.Domain;
using Carnavacs.Api.Infrastructure;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

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
        /// User Login. Returns JWT token and user info.
        /// </summary>
        /// <param name="login">LoginModel with username and password</param>
        /// <returns></returns>
        [HttpPost]
        [ProducesResponseType<ApiResponse<LoginResponse>>(StatusCodes.Status200OK)]
        [ProducesErrorResponseType(typeof(BadRequest))]
        [AllowAnonymous]
        public async Task<IActionResult> Login([FromBody] LoginModel login)
        {
            var response = new ApiResponse<LoginResponse>();
            try
            {
                response.Result = await _loginManager.Login(login);
                response.Success = true;
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(new ApiResponse<LoginResponse> { Success = false, Message = ex.Message });
            }
        }

        [HttpPost("Logout")]
        public async Task<IActionResult> Logout(string access_token)
        {
            return Ok(null);
        }

    }
}
