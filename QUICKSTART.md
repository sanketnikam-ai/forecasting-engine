# QUICK START GUIDE

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify installation (optional)
python -c "import pandas, numpy, sklearn; print('Basic packages OK')"
```

## Run Your First Forecast (3 Steps)

### Step 1: Prepare Your CSV File
Ensure your data has these columns:
```
date,value
2023-01-01,100
2023-01-02,105
2023-01-03,110
...
```

### Step 2: Run the Engine
```bash
python forecast_cli.py your_data.csv
```

### Step 3: Check Results
Look for:
- `forecast_results.csv` - All predictions
- `forecast_plot.png` - Visual comparison
- Console output showing best model

## Example with Sample Data

```bash
# Use included sample data
python forecast_cli.py sample_data.csv --test-size 0.3
```

## Python Script Usage

```python
from forecasting_engine import ForecastingEngine

# Load and forecast
engine = ForecastingEngine('your_data.csv')
engine.split_data(test_size=0.2)
engine.run_all_forecasts()

# See results
print(engine.get_metrics_summary())
best_model, metrics = engine.get_best_model()
print(f"Best: {best_model} - MAPE: {metrics['MAPE']:.2f}%")
```

## Common Issues

**"Package not found"**: Install the specific package
```bash
pip install statsmodels prophet xgboost tbats
```

**"Network error"**: Some packages require internet - install in a connected environment

**"Memory error with TFT"**: Normal - TFT needs more resources, other 5 methods will still work

## Method Cheat Sheet

| Method | Use When | Speed | Accuracy |
|--------|----------|-------|----------|
| SARIMA | Clear seasonality | Medium | High |
| Holt-Winters | Simple patterns | Fast | Good |
| TBATS | Multiple seasons | Slow | High |
| Prophet | Daily data + holidays | Medium | Good |
| XGBoost | Complex patterns | Fast | High |
| TFT | Lots of data | Slowest | Highest |

## Need Help?

1. Check README.md for detailed docs
2. Run `python forecast_cli.py --help`
3. See forecasting_tutorial.ipynb for examples
