using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Interfaces;
using Carnavacs.Api.Infrastructure;
using Carnavacs.Api.Infrastructure.Interfaces;
using Carnavacs.Api.Infrastructure.Services;
using Microsoft.AspNetCore.Mvc;
using Serilog;
using System.Reflection;

using Scalar.AspNetCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using Microsoft.OpenApi.Models;


var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

var sqlConn = builder.Configuration.GetConnectionString("Carnaval");
// Add services to the container.
builder.Services.AddSingleton<DapperContext>(new DapperContext(sqlConn));
builder.Services.AddSingleton<Carnavacs.Api.Infrastructure.TokenHandler>();

builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddScoped<LoginManager>();
builder.Services.AddScoped<IQuentroApiClient, QuentroApiClient>();
builder.Services.AddControllers();

//CORS-----------------------------
var specificOrgins = "AppOrigins";

builder.Services.AddCors(options =>
{
    options.AddPolicy(name: specificOrgins,
                      policy =>
                      {
                          policy.WithOrigins("http://localhost:3000").AllowAnyHeader().AllowAnyMethod();
                      });
});


builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
        };
    })
    .AddApiKeyAuthentication();

// Add authorization
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("RequireApiKey", policy =>
    {
        policy.AuthenticationSchemes.Add("ApiKey");
        policy.RequireAuthenticatedUser(); // Adding a requirement
    });
    options.AddPolicy("RequireJwt", policy =>
    {
        policy.AuthenticationSchemes.Add(JwtBearerDefaults.AuthenticationScheme);
        policy.RequireAuthenticatedUser(); // Adding a requirement
    });
});


// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi(options =>
{
    options.AddDocumentTransformer<BearerSecuritySchemeTransformer>();
});

// Add traditional Swagger UI alongside Scalar
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "Carnavacs API",
        Version = "v1",
        Description = "Carnaval ticket validation API"
    });

    // Add JWT Bearer token support
    c.AddSecurityDefinition("Bearer", new Microsoft.OpenApi.Models.OpenApiSecurityScheme
    {
        In = Microsoft.OpenApi.Models.ParameterLocation.Header,
        Description = "Please enter JWT with Bearer into field",
        Name = "Authorization",
        Type = Microsoft.OpenApi.Models.SecuritySchemeType.ApiKey
    });

    c.AddSecurityRequirement(new Microsoft.OpenApi.Models.OpenApiSecurityRequirement {
    {
        new Microsoft.OpenApi.Models.OpenApiSecurityScheme
        {
            Reference = new Microsoft.OpenApi.Models.OpenApiReference
            {
                Type = Microsoft.OpenApi.Models.ReferenceType.SecurityScheme,
                Id = "Bearer"
            }
        },
        new string[] { }
    }});
});


builder.Services.AddSingleton<INFCGenerator, NFCGenerator>();
builder.Services.AddHttpClient();
builder.Services.AddHostedService<TicketekMiddleware>();


var app = builder.Build();


//if (app.Environment.IsDevelopment())
//{
app.UseCors(specificOrgins);

// Add Swagger middleware
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Carnavacs API v1");
    c.RoutePrefix = "swagger"; // This makes /swagger the URL
});


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
