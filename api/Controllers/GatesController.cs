using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;

namespace Carnavacs.Api.Controllers
{
    public class GatesController : BaseApiController
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly ILogger<GatesController> _logger;

        public GatesController(IUnitOfWork unitOfWork, ILogger<GatesController> logger)
        {
            this._unitOfWork = unitOfWork;
            this._logger = logger;
        }


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


        [HttpGet("{id}")]
        public async Task<ApiResponse<Event>> GetById(int id)
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
