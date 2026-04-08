using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.ML.Data;
using Microsoft.Extensions.ML;
using System.IO;
using System.Threading.RateLimiting;
using Microsoft.AspNetCore.RateLimiting;
using System;

namespace GoldPrice_API
{
    public class ModelInput
    {
        [LoadColumn(1)] public float Open { get; set; }
        [LoadColumn(2)] public float High { get; set; }
        [LoadColumn(3)] public float Low { get; set; }
        [LoadColumn(6)] public float Volume { get; set; }
        
        [LoadColumn(4), ColumnName("Label")] public float Close { get; set; }
    }

    public class ModelOutput
    {
        [ColumnName("Score")] public float PredictedClose { get; set; }
    }

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
                options.AddPolicy("AllowAll",
                    builder =>
                    {
                        builder.AllowAnyOrigin()
                               .AllowAnyMethod()
                               .AllowAnyHeader();
                    });
            });

            // Path to the ML.NET model
            string modelPath = Path.Combine(Directory.GetCurrentDirectory(), "..", "GoldPrice_CLI", "GoldModel.zip");
            
            // Try fallback if starting from inside bin folder
            if (!File.Exists(modelPath))
            {
                // Fallback to absolute path or just assume it is in the same folder if copied
                string fallbackPath = Path.Combine(@"D:\Coding Space\Project\Group3\GoldPrice_CLI\GoldModel.zip");
                if (File.Exists(fallbackPath))
                {
                    modelPath = fallbackPath;
                }
            }

            // Register PredictionEnginePool
            builder.Services.AddPredictionEnginePool<ModelInput, ModelOutput>()
                .FromFile(modelName: "GoldModel", filePath: modelPath, watchForChanges: true);

            // Add Rate Limiting
            builder.Services.AddRateLimiter(options =>
            {
                options.AddFixedWindowLimiter("fixed", policy =>
                {
                    policy.PermitLimit = 5;
                    policy.Window = TimeSpan.FromSeconds(10);
                    policy.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
                    policy.QueueLimit = 2;
                });
                options.RejectionStatusCode = 429;
            });

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

            // Serve static files for our UI
            app.UseDefaultFiles();
            app.UseStaticFiles();

            // Setup Prediction API Endpoint
            app.MapPost("/predict", (PredictionEnginePool<ModelInput, ModelOutput> predictionEnginePool, ModelInput input) =>
            {
                var prediction = predictionEnginePool.Predict(modelName: "GoldModel", example: input);
                return Results.Ok(new { predictedClose = prediction.PredictedClose });
            })
            .WithName("PredictGoldPrice")
            .WithOpenApi()
            .RequireRateLimiting("fixed");

            app.Run();
        }
    }
}
