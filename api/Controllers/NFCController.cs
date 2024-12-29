using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace Carnavacs.Api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class NFCController : ControllerBase
    {


        private readonly ILogger<NFCController> _logger;
        private readonly INFCGenerator _nfcService;

        public NFCController(ILogger<NFCController> logger, INFCGenerator nFCGenerator)
        {
            _logger = logger;
            _nfcService = nFCGenerator;
        }

        [HttpGet(Name = "GetTicket")]
        public IActionResult Get()
        {
            var nfc = _nfcService.Get();
            return PhysicalFile(nfc, "application/octet-stream");
        }
    }
}
