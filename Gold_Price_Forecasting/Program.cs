using Gold_Price_Forecasting;

namespace Gold_Price_Forecasting
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            Console.WriteLine("╔══════════════════════════════════════════════════╗");
            Console.WriteLine("║         DỰ ĐOÁN GIÁ VÀNG (USO) - ML.NET          ║");
            Console.WriteLine("╚══════════════════════════════════════════════════╝");
            Console.WriteLine();

            int horizon = GetHorizonInput();

            Console.WriteLine();
            Console.WriteLine($"Đang dự đoán giá vàng cho {horizon} phiên tiếp theo...");
            Console.WriteLine();

            try
            {
                var modelOutput = GoldForecastingModel.Predict(horizon: horizon);

                PrintPredictionTable(modelOutput, horizon);
                PrintSummary(modelOutput);
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"❌ Lỗi khi dự đoán: {ex.Message}");
                Console.ResetColor();
            }

            Console.WriteLine();
            Console.WriteLine("Nhấn phím bất kỳ để thoát...");
            Console.ReadKey();
        }

        private static int GetHorizonInput()
        {
            while (true)
            {
                Console.Write("Nhập số phiên cần dự đoán (1-30, mặc định 5): ");
                string? input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                    return 5;

                if (int.TryParse(input, out int horizon) && horizon >= 1 && horizon <= 30)
                    return horizon;

                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("⚠ Vui lòng nhập số nguyên từ 1 đến 30.");
                Console.ResetColor();
            }
        }

        private static void PrintPredictionTable(GoldForecastingModel.ModelOutput output, int horizon)
        {
            string separator = "├──────────┼────────────────┼────────────────┼────────────────┤";
            string topBorder = "┌──────────┬────────────────┬────────────────┬────────────────┐";
            string bottomBorder = "└──────────┴────────────────┴────────────────┴────────────────┘";

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine(topBorder);
            Console.WriteLine($"│ {"Phiên",-8} │ {"Giá dự đoán",14} │ {"Cận dưới (LB)",14} │ {"Cận trên (UB)",14} │");
            Console.WriteLine(separator);
            Console.ResetColor();

            for (int i = 0; i < output.Close.Length; i++)
            {
                string predicted = $"{output.Close[i]:F2}$";
                string lb = $"{output.Close_LB[i]:F2}$";
                string ub = $"{output.Close_UB[i]:F2}$";

                Console.ForegroundColor = ConsoleColor.White;
                Console.Write($"│ {i + 1,-8} │ ");

                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write($"{predicted,14} ");

                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write($"│ {lb,14} ");

                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.Write($"│ {ub,14} ");

                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("│");
            }

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine(bottomBorder);
            Console.ResetColor();
        }

        private static void PrintSummary(GoldForecastingModel.ModelOutput output)
        {
            float avgPrice = output.Close.Average();
            float minPrice = output.Close.Min();
            float maxPrice = output.Close.Max();

            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("Tổng kết:");
            Console.ResetColor();
            Console.WriteLine($"   Giá trung bình dự đoán : {avgPrice:F2}$");
            Console.WriteLine($"   Giá thấp nhất dự đoán  : {minPrice:F2}$");
            Console.WriteLine($"   Giá cao nhất dự đoán   : {maxPrice:F2}$");
        }
    }
}
