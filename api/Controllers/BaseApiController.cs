using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Carnavacs.Api.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class BaseApiController : ControllerBase
    {
        protected string? getClientIP()
        {
            return HttpContext.GetServerVariable("HTTP_X_FORWARDED_FOR") ??
                            Request.Headers["HTTP_X_FORWARDED_FOR"].ToString() ??
                            HttpContext.Connection.RemoteIpAddress?.ToString();
        }
    }
}
