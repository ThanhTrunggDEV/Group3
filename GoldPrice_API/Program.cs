using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using GoldPrice_API.Extensions;
using GoldPrice_API.Endpoints;

namespace GoldPrice_API
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            builder.Services.AddCors(options =>
            {
                options.AddPolicy("AllowAll", builder =>
                {
                    builder.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader();
                });
            });

            // Clean Architecture Extensions
            builder.Services.AddCustomRateLimiting();
            builder.Services.AddGoldPriceModel();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment() || app.Environment.IsProduction())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseCors("AllowAll");
            
            // Apply Rate Limiter middleware
            app.UseRateLimiter();

            // Serve UI
            app.UseDefaultFiles();
            app.UseStaticFiles();

            // Map Endpoints
            app.MapPredictionEndpoints();

            app.Run();
        }
    }
}
