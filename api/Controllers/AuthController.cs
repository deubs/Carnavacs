using Carnavacs.Api.Controllers.Helpers;
using Microsoft.AspNetCore.Mvc;

namespace Carnavacs.Api.Controllers
{
    [Produces("application/json")]
    [Route("[controller]")]
    [ApiExplorerSettings(IgnoreApi = true)]

    [SwaggerControllerOrder(1)]
    public class AuthController : Controller
    {
        [HttpGet]
        public IActionResult NotAuthorized()
        {
            return Unauthorized();
        }
    }
}
