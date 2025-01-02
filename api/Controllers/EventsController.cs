using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using System.ComponentModel;

namespace Carnavacs.Api.Controllers
{

    public class EventsController : BaseApiController
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly ILogger<EventsController> _logger;

        public EventsController(IUnitOfWork unitOfWork, ILogger<EventsController> logger)
        {
            this._unitOfWork = unitOfWork;
            this._logger = logger;
        }


        [EndpointName("GetEvents")]
        [EndpointSummary("Get All Events")]
        [EndpointDescription("Get All Enabled event for current edition")]
        [HttpGet]
        public async Task<ApiResponse<List<Event>>> GetAll()
        {
            var apiResponse = new ApiResponse<List<Event>>();

            try
            {
                var data = await _unitOfWork.Events.GetAllAsync();
                apiResponse.Success = true;
                apiResponse.Result = data.ToList();
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all events");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all events");
            }

            return apiResponse;
        }

        [HttpGet("Current")]
        [EndpointName("GetCurrentEvent")]
        [EndpointSummary("Get Current Event")]
        [EndpointDescription("Get next available event")]

        [ProducesResponseType<ApiResponse<Event>>(StatusCodes.Status200OK, "application/json")]
        public async Task<ApiResponse<Event>> GetCurrent()
        {
            var apiResponse = new ApiResponse<Event>();

            try
            {
                var data = await _unitOfWork.Events.GetCurrentAsync();
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all events");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all events");
            }

            return apiResponse;
        }


        [Authorize(Policy = "RequireJwt")]
        [HttpGet("Stats")]
        [EndpointName("GetEventStats")]
        [EndpointSummary("Get Stats for current Event")]
        [EndpointDescription("Get information about the event.")]

        [ProducesResponseType<ApiResponse<Event>>(StatusCodes.Status200OK, "application/json")]
        public async Task<ApiResponse<EventStats>> GetStats()
        {
            var apiResponse = new ApiResponse<EventStats>();

            try
            {
                var data = await _unitOfWork.Events.GetStatsAsync();
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting event stats");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting event stats");
            }

            return apiResponse;
        }


        [HttpGet("{id}")]
        [ApiExplorerSettings(IgnoreApi = true)]
        public async Task<ApiResponse<Event>> GetById([Description("Auto generated id")] int id)
        {

            var apiResponse = new ApiResponse<Event>();

            try
            {
                var data = await _unitOfWork.Events.GetByIdAsync(id);
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting event by id");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting event by id");
            }

            return apiResponse;
        }

        [HttpPost]
        [ApiExplorerSettings(IgnoreApi = true)]
        public async Task<ApiResponse<string>> Add(Event Event)
        {
            var apiResponse = new ApiResponse<string>();

            try
            {
                var data = await _unitOfWork.Events.AddAsync(Event);
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "error adding event");
            }

            return apiResponse;
        }

        [HttpPut]
        [ApiExplorerSettings(IgnoreApi = true)]
        public async Task<ApiResponse<string>> Update(Event Event)
        {
            var apiResponse = new ApiResponse<string>();

            try
            {
                var data = await _unitOfWork.Events.UpdateAsync(Event);
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "error updating event");
            }

            return apiResponse;
        }

        [HttpDelete]
        [ApiExplorerSettings(IgnoreApi = true)]
        public async Task<ApiResponse<string>> Delete(int id)
        {
            var apiResponse = new ApiResponse<string>();

            try
            {
                var data = await _unitOfWork.Events.DeleteAsync(id);
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "error deleting event");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "error deleting event");
            }

            return apiResponse;
        }

    }
}
