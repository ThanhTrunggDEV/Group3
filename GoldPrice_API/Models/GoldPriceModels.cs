using Microsoft.ML.Data;

namespace GoldPrice_API.Models
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
}
