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
        [EndpointName("ValidateTicket")]
        [EndpointSummary("Validate a ticket and return result")]
        [EndpointDescription("Check if ticket is valid or not, and mark as used")]
        //[Authorize(Policy = "RequireApiKey")]
        public async Task<ApiResponse<TicketValidationResult>> Validate(string code)
        {
            var apiResponse = new ApiResponse<TicketValidationResult> { Success=true };

            /// True to mark the ticket as used and prevent reuse; false for a read-only validation
            bool persist = _configuration.GetValue<bool>("Persist");
            string? clientIP = getClientIP();

            try
            {
                // readOnly: false - this burns the ticket in Quentro API
                apiResponse.Result = await _unitOfWork.Tickets.ValidateAsync(code, readOnly: false, deviceId: clientIP);
                
                if (apiResponse.Result.Persist && persist)
                {
                    if (apiResponse.Result.IsQuentro)
                    {
                        // Quentro ticket: already burned by API, just log the read with ticket type for sector stats
                        await _unitOfWork.Tickets.LogQuentroAsync(code, clientIP, apiResponse.Result.TicketStatus, apiResponse.Result.TicketType);
                    }
                    else
                    {
                        // Old system ticket: mark as used and log
                        await _unitOfWork.Tickets.UseAsync(code, clientIP);
                    }
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

        [HttpPost("Verify")]
        //[Authorize(Policy = "RequireApiKey")]
        [EndpointName("VerifyTicket")]
        [EndpointSummary("Check ticket status and return result")]
        [EndpointDescription("Check if ticket is valid or not, readonly, doesn't change status")]
        public async Task<ApiResponse<TicketValidationResult>> Verify(string code)
        {
            var apiResponse = new ApiResponse<TicketValidationResult> { Success = true };

            try
            {
                // readOnly: true - uses /check endpoint, doesn't burn the ticket
                apiResponse.Result = await _unitOfWork.Tickets.ValidateAsync(code, readOnly: true, deviceId: getClientIP());
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
