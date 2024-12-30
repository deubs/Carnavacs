using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Interfaces;
using Carnavacs.Api.Infrastructure;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Serilog;
using System.Reflection;

using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

var sqlConn = builder.Configuration.GetConnectionString("Carnaval");
// Add services to the container.
builder.Services.AddSingleton<DapperContext>(new DapperContext(sqlConn));
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();

builder.Services.AddControllers();
SwaggerControllerOrder<ControllerBase> swaggerControllerOrder = new SwaggerControllerOrder<ControllerBase>(Assembly.GetEntryAssembly());


//builder.Services.AddAuthentication().AddJwtBearer();
//builder.Services.AddAuthorization(o =>
//{
//    o.AddPolicy("ApiTesterPolicy", b => b.RequireRole("tester"));
//});
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi(options =>
{
    options.AddDocumentTransformer<BearerSecuritySchemeTransformer>();
});

builder.Services.AddSingleton<INFCGenerator, NFCGenerator>();

var app = builder.Build();


//if (app.Environment.IsDevelopment())
//{
    app.MapOpenApi()
            //.RequireAuthorization("ApiTesterPolicy");
    ;
app.MapScalarApiReference(options =>
{
    // Fluent API
    options
        .WithPreferredScheme("ApiKey") // Optional. Security scheme name from the OpenAPI document
        .WithApiKeyAuthentication(apiKey =>
        {
            apiKey.Token = "your-api-key";
        });

    // Object initializer
    options.Authentication = new ScalarAuthenticationOptions
    {
        PreferredSecurityScheme = "ApiKey", // Optional. Security scheme name from the OpenAPI document
        ApiKey = new ApiKeyOptions
        {
            Token = "your-api-key"
        }
    };
});
//}


app.UseAuthorization();

app.MapControllers();
app.UseSerilogRequestLogging();
app.Run();
