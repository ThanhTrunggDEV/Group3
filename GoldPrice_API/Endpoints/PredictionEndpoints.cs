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

            apiGroup.MapPost("/", async (PredictionEnginePool<ModelInput, ModelOutput> predictionEnginePool, ModelInput input, System.Net.Http.IHttpClientFactory httpClientFactory) =>
            {
                var prediction = predictionEnginePool.Predict(modelName: "GoldModel", example: input);
                
                // Fetch external APIs (Test 3 Requirement: Sử dụng API từ các nguồn khác)
                var client = httpClientFactory.CreateClient();
                float liveWorldPrice = 0f;
                float vndRate = 25000f; // Tỉ giá dự phòng

                try 
                {
                    // 1. Lấy giá Vàng sát thực tế (PAXG neo giá vàng) từ Binance
                    var binanceResponse = await client.GetAsync("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT");
                    if (binanceResponse.IsSuccessStatusCode)
                    {
                        var json = await binanceResponse.Content.ReadAsStringAsync();
                        var doc = System.Text.Json.JsonDocument.Parse(json);
                        var priceStr = doc.RootElement.GetProperty("price").GetString();
                        if (float.TryParse(priceStr, System.Globalization.NumberStyles.Any, System.Globalization.CultureInfo.InvariantCulture, out float p))
                            liveWorldPrice = p;
                    }

                    // 2. Lấy tỷ giá ngoại tệ thật (USD -> VND) từ Exchange API
                    var erResponse = await client.GetAsync("https://open.er-api.com/v6/latest/USD");
                    if (erResponse.IsSuccessStatusCode)
                    {
                        var json = await erResponse.Content.ReadAsStringAsync();
                        var doc = System.Text.Json.JsonDocument.Parse(json);
                        vndRate = doc.RootElement.GetProperty("rates").GetProperty("VND").GetSingle();
                    }
                }
                catch 
                {
                    // Bỏ qua lỗi nếu API bên thứ 3 chết để duy trì server chạy bình thường
                }

                return Results.Ok(new 
                { 
                    success = true,
                    data = new 
                    { 
                        predictedClose = prediction.PredictedClose,
                        predictedCloseVnd = prediction.PredictedClose * vndRate,
                        liveWorldPrice = liveWorldPrice,
                        exchangeRateVnd = vndRate
                    }
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
