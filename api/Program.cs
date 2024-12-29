using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Interfaces;
using Carnavacs.Api.Infrastructure;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.OpenApi.Models;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

var sqlConn = builder.Configuration.GetConnectionString("Carnaval");
// Add services to the container.
builder.Services.AddSingleton<DapperContext>(new DapperContext(sqlConn));
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(
  c =>
  {
      c.AddSecurityDefinition("basic", new OpenApiSecurityScheme
      {
          Description = "api key.",
          Name = "Authorization",
          In = ParameterLocation.Header,
          Type = SecuritySchemeType.ApiKey,
          Scheme = "basic"
      });

      c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "basic"
                },
                In = ParameterLocation.Header
            },
            new List<string>()
        }
    });
  });

builder.Services.AddSingleton<INFCGenerator, NFCGenerator>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}



app.UseAuthorization();

app.MapControllers();
app.UseSerilogRequestLogging();
app.Run();
