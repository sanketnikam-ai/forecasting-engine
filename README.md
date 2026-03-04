# Forecasting Engine

A comprehensive time series forecasting engine that supports 6 different forecasting methods:

1. **SARIMA** - Seasonal AutoRegressive Integrated Moving Average
2. **Holt-Winters** - Exponential Smoothing
3. **TBATS** - Trigonometric, Box-Cox, ARMA, Trend, Seasonal
4. **Prophet** - Facebook's forecasting model
5. **XGBoost** - Gradient Boosting for time series
6. **TFT** - Temporal Fusion Transformer (Deep Learning)

## Features

- ✅ Multiple forecasting methods in one engine
- ✅ Automatic model comparison with performance metrics
- ✅ CSV input/output support
- ✅ Visualization of forecasts
- ✅ Easy-to-use CLI interface
- ✅ Python API for programmatic use
- ✅ Automatic train/test splitting
- ✅ Performance metrics (MAE, RMSE, MAPE)

## Installation

```bash
# Install required packages
pip install -r requirements.txt
```

## Quick Start

### Using the CLI

```bash
# Basic usage
python forecast_cli.py your_data.csv

# With custom parameters
python forecast_cli.py your_data.csv \
    --date-col "Date" \
    --value-col "Sales" \
    --freq "M" \
    --test-size 0.2 \
    --output results.csv \
    --plot forecast_plot.png

# Run specific methods only
python forecast_cli.py your_data.csv --methods SARIMA Prophet XGBoost
```

### Using the Python API

```python
from forecasting_engine import ForecastingEngine

# Initialize with your CSV file
engine = ForecastingEngine(
    data_path='your_data.csv',
    date_col='date',
    value_col='value',
    freq='D'  # D=daily, W=weekly, M=monthly
)

# Split data into train/test
engine.split_data(test_size=0.2)

# Run all forecasting methods
engine.run_all_forecasts()

# Get performance metrics
print(engine.get_metrics_summary())

# Get best model
best_model, metrics = engine.get_best_model()
print(f"Best model: {best_model}")
print(f"MAPE: {metrics['MAPE']:.2f}%")

# Export results
engine.export_results('forecast_results.csv')
```

### Running Individual Methods

```python
# Run SARIMA
engine.forecast_sarima(order=(1,1,1), seasonal_order=(1,1,1,12))

# Run Holt-Winters
engine.forecast_holtwinters(seasonal='add', seasonal_periods=12)

# Run TBATS
engine.forecast_tbats(use_box_cox=True)

# Run Prophet
engine.forecast_prophet(yearly_seasonality=True, weekly_seasonality=True)

# Run XGBoost
engine.forecast_xgboost(n_lags=12)

# Run TFT
engine.forecast_tft(max_encoder_length=60, max_prediction_length=30)
```

## Input Data Format

Your CSV file should have at least two columns:

```csv
date,value
2022-01-01,105.23
2022-01-02,107.45
2022-01-03,109.12
...
```

- **date**: Date column in any format pandas can parse
- **value**: Numerical values to forecast

## Method Descriptions

### 1. SARIMA
- **Best for**: Data with trend and clear seasonal patterns
- **Parameters**: 
  - `order=(p,d,q)`: Non-seasonal order
  - `seasonal_order=(P,D,Q,s)`: Seasonal order
- **Pros**: Interpretable, well-established theory
- **Cons**: Requires manual parameter tuning

### 2. Holt-Winters
- **Best for**: Data with trend and seasonality, simpler than SARIMA
- **Parameters**:
  - `seasonal`: 'add' or 'mul' (additive or multiplicative)
  - `seasonal_periods`: Length of seasonal cycle
- **Pros**: Simple, fast, good baseline
- **Cons**: Limited to specific patterns

### 3. TBATS
- **Best for**: Complex seasonality (multiple seasonal periods)
- **Parameters**:
  - `use_box_cox`: Apply Box-Cox transformation
- **Pros**: Handles multiple seasonality, automatic
- **Cons**: Slower than simpler methods

### 4. Prophet
- **Best for**: Daily data with holidays and strong seasonality
- **Parameters**:
  - `yearly_seasonality`, `weekly_seasonality`, `daily_seasonality`
- **Pros**: Handles holidays, missing data, outliers
- **Cons**: May overfit on small datasets

### 5. XGBoost
- **Best for**: Non-linear patterns, complex relationships
- **Parameters**:
  - `n_lags`: Number of lag features
  - XGBoost hyperparameters
- **Pros**: Captures complex patterns, feature importance
- **Cons**: Requires feature engineering

### 6. TFT (Temporal Fusion Transformer)
- **Best for**: Long sequences, complex temporal patterns
- **Parameters**:
  - `max_encoder_length`: Input sequence length
  - `max_prediction_length`: Forecast horizon
- **Pros**: State-of-art performance, handles long sequences
- **Cons**: Requires more data, computationally expensive

## Performance Metrics

The engine calculates three key metrics:

- **MAE** (Mean Absolute Error): Average absolute difference
- **RMSE** (Root Mean Squared Error): Emphasizes large errors
- **MAPE** (Mean Absolute Percentage Error): Percentage error

Lower values indicate better performance.

## Output Files

### forecast_results.csv
Contains all forecasts compared with actual values:

```csv
date,actual,SARIMA,HoltWinters,TBATS,Prophet,XGBoost,TFT
2022-11-01,150.23,148.45,149.12,151.34,...
...
```

### forecast_plot.png
Visualization showing:
- Training data (black line)
- Actual test data (blue line)
- Forecasts from all methods (colored dashed lines)

## Advanced Usage

### Custom Train/Test Split

```python
# Use first 80% for training
engine.split_data(test_size=0.2)

# Or manually specify split point
split_date = '2022-10-01'
engine.train = engine.df[:split_date]
engine.test = engine.df[split_date:]
```

### Forecasting Future Periods

```python
# Forecast 30 days beyond your data
engine.forecast_sarima(forecast_periods=30)
```

### Using with DataFrame

```python
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Initialize engine with DataFrame
engine = ForecastingEngine(df=df, date_col='Date', value_col='Sales')
```

### Parameter Tuning

```python
# SARIMA with custom parameters
engine.forecast_sarima(
    order=(2, 1, 2),
    seasonal_order=(1, 1, 1, 7)  # Weekly seasonality
)

# XGBoost with custom hyperparameters
engine.forecast_xgboost(
    n_lags=24,
    n_estimators=200,
    max_depth=7,
    learning_rate=0.05
)
```

## Troubleshooting

### "Package not available" errors

If you see warnings about missing packages:

```bash
# Install specific package
pip install statsmodels  # For SARIMA, Holt-Winters
pip install tbats        # For TBATS
pip install prophet      # For Prophet
pip install xgboost      # For XGBoost
pip install pytorch-forecasting pytorch-lightning  # For TFT
```

### Memory issues with TFT

TFT requires significant memory. For large datasets:
- Reduce `max_encoder_length`
- Reduce `batch_size`
- Use a subset of your data

### Poor performance

- Check data quality (missing values, outliers)
- Try different train/test splits
- Tune model parameters
- Ensure appropriate frequency is set

## Examples

See the included files:
- `sample_data.csv`: Example time series data
- `forecasting_engine.py`: Main engine code with usage examples

## Requirements

- Python 3.8+
- pandas, numpy, scikit-learn
- statsmodels (for SARIMA, Holt-Winters)
- tbats (for TBATS)
- prophet (for Prophet)
- xgboost (for XGBoost)
- pytorch, pytorch-lightning, pytorch-forecasting (for TFT)

## License

MIT License - feel free to use for any purpose.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example usage in the code
3. Ensure all dependencies are installed correctly

## Tips for Best Results

1. **Choose the right frequency**: Match your data's natural interval
2. **Sufficient history**: More data generally = better forecasts
3. **Clean your data**: Handle missing values and outliers
4. **Compare methods**: Different methods excel with different patterns
5. **Validate properly**: Use appropriate train/test split
6. **Consider seasonality**: Match seasonal parameters to your data
7. **Start simple**: Try simpler methods (Holt-Winters) before complex ones (TFT)

Happy Forecasting! 📈
