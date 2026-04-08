using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.ML;
using GoldPrice_API.Models;

namespace GoldPrice_API.Endpoints
{
    public static class PredictionEndpoints
    {
        public static WebApplication MapPredictionEndpoints(this WebApplication app)
        {
            app.MapPost("/predict", (PredictionEnginePool<ModelInput, ModelOutput> predictionEnginePool, ModelInput input) =>
            {
                var prediction = predictionEnginePool.Predict(modelName: "GoldModel", example: input);
                return Results.Ok(new { predictedClose = prediction.PredictedClose });
            })
            .WithName("PredictGoldPrice")
            .WithOpenApi()
            .RequireRateLimiting("fixed");

            return app;
        }
    }
}
