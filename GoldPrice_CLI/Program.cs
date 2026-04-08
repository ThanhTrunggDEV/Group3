using System;
using Microsoft.ML;
using Microsoft.ML.Data;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace GoldPrice_CLI
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

    class Program
    {
        private static string DataPath = "";
        private static string ModelPath = Path.Combine(Directory.GetCurrentDirectory(), "GoldModel.zip");

        static void Main(string[] args)
        {
            Console.WriteLine("=========================================================");
            Console.WriteLine("  Advanced Gold Price Forecasting CLI - LightGBM         ");
            Console.WriteLine("=========================================================\n");

            DataPath = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).FullName, "FINAL_USO.csv");
            if (!File.Exists(DataPath))
            {
                DataPath = @"D:\Coding Space\Project\Group3\FINAL_USO.csv";
            }

            var mlContext = new MLContext(seed: 42);
            ITransformer model;

            Console.WriteLine("1. Loading and Preparing Data...");
            IDataView dataView = mlContext.Data.LoadFromTextFile<ModelInput>(
                path: DataPath,
                hasHeader: true,
                separatorChar: ',');

            var trainTestData = mlContext.Data.TrainTestSplit(dataView, testFraction: 0.2);

            Console.WriteLine("2. Starting Training Process (LightGBM)...");
            model = TrainModel(mlContext, trainTestData.TrainSet);

            Console.WriteLine("\n3. Saving the Trained Model...");
            mlContext.Model.Save(model, trainTestData.TrainSet.Schema, ModelPath);
            Console.WriteLine($"   [OK] Model successfully saved to {ModelPath}");

            Console.WriteLine("\n4. Evaluating the Model...");
            EvaluateModel(mlContext, model, trainTestData.TestSet);

            Console.WriteLine("\n5. Entering Interactive Prediction Mode...");
            RunInteractivePrediction(mlContext, model);
        }

        private static ITransformer TrainModel(MLContext mlContext, IDataView trainData)
        {
            int iterations = 1000;
            double learningRate = 0.005;
            var pipeline = mlContext.Transforms.Concatenate("Features", 
                    nameof(ModelInput.Open), 
                    nameof(ModelInput.High), 
                    nameof(ModelInput.Low), 
                    nameof(ModelInput.Volume))
                .Append(mlContext.Regression.Trainers.LightGbm(labelColumnName: "Label", featureColumnName: "Features", learningRate: learningRate, numberOfIterations: iterations));

            return pipeline.Fit(trainData);
        }

        private static void EvaluateModel(MLContext mlContext, ITransformer model, IDataView testData)
        {
            var predictions = model.Transform(testData);
            var metrics = mlContext.Regression.Evaluate(predictions, labelColumnName: "Label", scoreColumnName: "Score");

            Console.WriteLine("--- Model Evaluation Metrics ---");
            Console.WriteLine($"* R-Squared (R2)                 : {metrics.RSquared:0.####}");
            Console.WriteLine($"* Mean Absolute Error (MAE)      : {metrics.MeanAbsoluteError:0.####}");
            Console.WriteLine($"* Root Mean Squared Error (RMSE) : {metrics.RootMeanSquaredError:0.####}");
            Console.WriteLine("--------------------------------");

            // Print 5 sample accurate random predictions
            var testDataEnumerable = mlContext.Data.CreateEnumerable<ModelInput>(testData, reuseRowObject: false).Take(5).ToList();
            var predictionEngine = mlContext.Model.CreatePredictionEngine<ModelInput, ModelOutput>(model);

            Console.WriteLine("\n--- Sample Test Predictions (First 5 records) ---");
            foreach (var sample in testDataEnumerable)
            {
                var prediction = predictionEngine.Predict(sample);
                Console.WriteLine($"Actual: {sample.Close,8:0.00} | Predicted: {prediction.PredictedClose,8:0.00} | Diff: {Math.Abs(sample.Close - prediction.PredictedClose),6:0.00}");
            }
        }

        private static void RunInteractivePrediction(MLContext mlContext, ITransformer model)
        {
            var predictionEngine = mlContext.Model.CreatePredictionEngine<ModelInput, ModelOutput>(model);

            while (true)
            {
                Console.WriteLine("\n================ Interactive Mode ==================");
                Console.WriteLine("Enter values to predict Gold 'Close' price (or type 'exit' to quit):");

                try
                {
                    Console.Write("> Enter 'Open' price: ");
                    string openStr = Console.ReadLine();
                    if (openStr?.ToLower() == "exit") break;
                    float openInfo = float.Parse(openStr);

                    Console.Write("> Enter 'High' price: ");
                    string highStr = Console.ReadLine();
                    if (highStr?.ToLower() == "exit") break;
                    float highInfo = float.Parse(highStr);

                    Console.Write("> Enter 'Low' price: ");
                    string lowStr = Console.ReadLine();
                    if (lowStr?.ToLower() == "exit") break;
                    float lowInfo = float.Parse(lowStr);

                    Console.Write("> Enter 'Volume'    : ");
                    string volStr = Console.ReadLine();
                    if (volStr?.ToLower() == "exit") break;
                    float volumeInfo = float.Parse(volStr);

                    var sample = new ModelInput
                    {
                        Open = openInfo,
                        High = highInfo,
                        Low = lowInfo,
                        Volume = volumeInfo
                    };

                    var prediction = predictionEngine.Predict(sample);

                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"\n[RESULT] The predicted 'Close' price is: {prediction.PredictedClose:0.00} USD");
                    Console.ResetColor();
                }
                catch (FormatException)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("[ERROR] Invalid input! Please enter numeric values only.");
                    Console.ResetColor();
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"[ERROR] An error occurred: {ex.Message}");
                    Console.ResetColor();
                }
            }
            Console.WriteLine("Exiting Interactive Mode. Goodbye!");
        }
    }
}
