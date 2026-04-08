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
            // Tách Group API v1 rõ ràng theo chuẩn RESTful
            var apiGroup = app.MapGroup("/api/v1/predictions")
                              .WithTags("Predictions");

            apiGroup.MapPost("/", (PredictionEnginePool<ModelInput, ModelOutput> predictionEnginePool, ModelInput input) =>
            {
                var prediction = predictionEnginePool.Predict(modelName: "GoldModel", example: input);
                return Results.Ok(new 
                { 
                    success = true,
                    data = new { predictedClose = prediction.PredictedClose }
                });
            })
            .WithName("CreateGoldPricePrediction")
            .WithOpenApi(operation => new(operation) 
            { 
                Summary = "Tạo một dự báo giá Vàng mới", 
                Description = "Gửi các thông số OHLC để nhận kết quả mô hình AI." 
            })
            .RequireRateLimiting("fixed");

            return app;
        }
    }
}
