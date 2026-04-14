using Microsoft.AspNetCore.RateLimiting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.ML;
using System;
using System.IO;
using System.Threading.RateLimiting;
using GoldPrice_API.Models;

namespace GoldPrice_API.Extensions
{
    public static class ServiceExtensions
    {
        public static IServiceCollection AddCustomRateLimiting(this IServiceCollection services)
        {
            services.AddRateLimiter(options =>
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
            
            // Enable HTTP Client for calling external 3rd-party APIs
            services.AddHttpClient();

            return services;
        }

        public static IServiceCollection AddGoldPriceModel(this IServiceCollection services)
        {
            // Path to the ML.NET model
            string modelPath = Path.Combine(Directory.GetCurrentDirectory(), "..", "GoldPrice_CLI", "GoldModel.zip");
            
            // Try fallback if starting from inside bin folder
            if (!File.Exists(modelPath))
            {
                string fallbackPath = Path.Combine(@"D:\Coding Space\Project\Group3\GoldPrice_CLI\GoldModel.zip");
                if (File.Exists(fallbackPath))
                {
                    modelPath = fallbackPath;
                }
            }

            // Register PredictionEnginePool
            services.AddPredictionEnginePool<ModelInput, ModelOutput>()
                .FromFile(modelName: "GoldModel", filePath: modelPath, watchForChanges: true);

            return services;
        }
    }
}
