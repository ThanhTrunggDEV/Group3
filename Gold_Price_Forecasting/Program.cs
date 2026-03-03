namespace BitCoin_Price_Forecasting
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var modelOutput = BitcoinForecastingModel.Predict();

            Console.Write("Nhap so gio de du doan: ");

            int horizion = int.Parse(Console.ReadLine() ?? "5");

            // predict next 5 periods
            modelOutput = BitcoinForecastingModel.Predict(horizon: horizion);
            Console.WriteLine(string.Join("\n", modelOutput.Close));

            Console.WriteLine("This is group 3");
            Console.WriteLine("Hello, World!");
        }
    }
}
