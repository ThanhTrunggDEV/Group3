using Gold_Price_Forecasting;

namespace BitCoin_Price_Forecasting
{
    internal class Program
    {
        static void Main(string[] args)
        {
            

            Console.Write("Nhap so gio de du doan: ");

            int horizion = int.Parse(Console.ReadLine() ?? "5");

          
            var modelOutput = GoldForecastingModel.Predict(horizon: horizion);

            for(int i = 0; i < modelOutput.Close.Length; i++)
            {
                Console.WriteLine($"Predicted Close Price[{i}]: {modelOutput.Close[i]}$ || LB: {modelOutput.Close_LB[i]}$ || UB: {modelOutput.Close_UB[i]}$");
            }


        }
    }
}
