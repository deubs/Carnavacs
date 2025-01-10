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
            if (!String.IsNullOrEmpty(HttpContext.GetServerVariable("HTTP_X_FORWARDED_FOR")))
                return HttpContext.GetServerVariable("HTTP_X_FORWARDED_FOR");
            if (!String.IsNullOrEmpty(Request.Headers["HTTP_X_FORWARDED_FOR"]))
                return Request.Headers["HTTP_X_FORWARDED_FOR"].ToString();
            return HttpContext.Connection.RemoteIpAddress?.ToString();
        }
    }
}
