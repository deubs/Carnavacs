using Microsoft.AspNetCore.Mvc;

namespace Carnavacs.Api.Controllers
{
    [Route("[controller]")]
    [TypeFilter(typeof(AuthorizationFilterAttribute))]
    [ApiController]
    public class BaseApiController : ControllerBase
    {
    }
}
