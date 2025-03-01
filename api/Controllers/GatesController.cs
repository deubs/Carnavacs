using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using System.ComponentModel;

namespace Carnavacs.Api.Controllers
{
    [SwaggerControllerOrder(4)]

    public class GatesController : BaseApiController
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly ILogger<GatesController> _logger;

        public GatesController(IUnitOfWork unitOfWork, ILogger<GatesController> logger)
        {
            this._unitOfWork = unitOfWork;
            this._logger = logger;
        }


        [EndpointName("GetGates")]
        [EndpointSummary("Get All Gates")]
        [EndpointDescription("Get All Enabled Gates for current edition")]
        [HttpGet ("Gates")]
        public async Task<ApiResponse<List<Gate>>> GetAll()
        {
            var apiResponse = new ApiResponse<List<Gate>>();

            try
            {
                var data = await _unitOfWork.Gates.GetAllAsync();
                apiResponse.Success = true;
                apiResponse.Result = data.ToList();
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all gates");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all Gates");
            }

            return apiResponse;
        }

        [EndpointName("GetDevices")]
        [EndpointSummary("Get All Devices in use")]
        [EndpointDescription("Get All Enabled Access Devices for current edition")]
        [HttpGet("Devices")]
        public async Task<ApiResponse<List<AccessDevice>>> GetAllDevices()
        {
            var apiResponse = new ApiResponse<List<AccessDevice>>();

            try
            {
                var data = await _unitOfWork.Gates.GetAllDevicesAsync();
                apiResponse.Success = true;
                apiResponse.Result = data.ToList();
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all gates");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting all Gates");
            }

            return apiResponse;
        }

        [HttpGet("{id}")]
        public async Task<ApiResponse<Gate>> GetById([Description("The gate id")] int id)
        {

            var apiResponse = new ApiResponse<Gate>();

            try
            {
                var data = await _unitOfWork.Gates.GetByIdAsync(id);
                apiResponse.Success = true;
                apiResponse.Result = data;
            }
            catch (SqlException ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting Gate by id");
            }
            catch (Exception ex)
            {
                apiResponse.Success = false;
                apiResponse.Message = ex.Message;
                _logger.LogError(ex, "Error getting Gate by id");
            }

            return apiResponse;
        }

    }
}
