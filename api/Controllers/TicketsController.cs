using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using Serilog.Core;
using System.Diagnostics;

namespace Carnavacs.Api.Controllers
{

    public class TicketController : BaseApiController
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly ILogger<TicketController> _logger;
        private readonly IConfiguration _configuration;

        public TicketController(IUnitOfWork unitOfWork, ILogger<TicketController> logger, IConfiguration configuration)
        {
            this._unitOfWork = unitOfWork;
            this._logger = logger;
            _configuration = configuration;
        }


        [HttpPost("Validate")]
        //[Authorize(Policy = "RequireApiKey")]
        public async Task<ApiResponse<TicketValidationResult>> Validate(string code)
        {
            var apiResponse = new ApiResponse<TicketValidationResult> { Success=true };

            /// True to mark the ticket as used and prevent reuse; false for a read-only validation
            bool persist = _configuration.GetValue<bool>("Persist");

            try
            {
                apiResponse.Result = await _unitOfWork.Tickets.ValidateAsync(code);
                if (apiResponse.Result.Persist && persist)
                {
                    await _unitOfWork.Tickets.UseAsync(apiResponse.Result.TicketId, getClientIP());
                    _unitOfWork.Commit();
                }

            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = "Unexpected Exception";
                _logger.LogError(ex, "Error validating ticket");
            }

            return apiResponse;
        }

    }
}
