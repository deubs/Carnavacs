using Carnavacs.Api.Controllers.Helpers;
using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Interfaces;
using Carnavacs.Api.Infrastructure;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Serilog;
using System.Reflection;

using Scalar.AspNetCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;


var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

var sqlConn = builder.Configuration.GetConnectionString("Carnaval");
// Add services to the container.
builder.Services.AddSingleton<DapperContext>(new DapperContext(sqlConn));
builder.Services.AddSingleton<Carnavacs.Api.Infrastructure.TokenHandler>();

builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddScoped<LoginManager>();
builder.Services.AddControllers();


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
