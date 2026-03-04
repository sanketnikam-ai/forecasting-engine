"""
Simple CLI interface for the Forecasting Engine
"""

import argparse
from forecasting_engine import ForecastingEngine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')


def plot_forecasts(engine, save_path='forecast_plot.png'):
    """Create visualization of all forecasts"""
    if not engine.results:
        print("No results to plot.")
        return
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot actual values
    ax.plot(engine.train.index, engine.train[engine.value_col], 
            label='Train', color='black', linewidth=2)
    ax.plot(engine.test.index, engine.test[engine.value_col], 
            label='Actual', color='blue', linewidth=2)
    
    # Plot forecasts
    colors = ['red', 'green', 'orange', 'purple', 'brown', 'pink']
    for i, (method, result) in enumerate(engine.results.items()):
        forecast = result['forecast']
        ax.plot(engine.test.index[:len(forecast)], forecast, 
                label=method, color=colors[i % len(colors)], 
                linestyle='--', linewidth=1.5, alpha=0.7)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title('Forecasting Methods Comparison', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {save_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Forecasting Engine CLI')
    parser.add_argument('input_file', help='Path to input CSV file')
    parser.add_argument('--date-col', default='date', help='Name of date column')
    parser.add_argument('--value-col', default='value', help='Name of value column')
    parser.add_argument('--freq', default='D', help='Frequency (D=daily, W=weekly, M=monthly)')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test set proportion')
    parser.add_argument('--methods', nargs='+', 
                       choices=['SARIMA', 'HoltWinters', 'TBATS', 'Prophet', 'XGBoost', 'TFT'],
                       help='Specific methods to run (default: all)')
    parser.add_argument('--output', default='forecast_results.csv', help='Output CSV file')
    parser.add_argument('--plot', default='forecast_plot.png', help='Output plot file')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("FORECASTING ENGINE")
    print("=" * 60)
    print(f"\nInput file: {args.input_file}")
    print(f"Date column: {args.date_col}")
    print(f"Value column: {args.value_col}")
    print(f"Frequency: {args.freq}")
    print(f"Test size: {args.test_size * 100}%")
    
    # Initialize engine
    engine = ForecastingEngine(
        data_path=args.input_file,
        date_col=args.date_col,
        value_col=args.value_col,
        freq=args.freq
    )
    
    # Split data
    engine.split_data(test_size=args.test_size)
    print(f"\nTrain samples: {len(engine.train)}")
    print(f"Test samples: {len(engine.test)}")
    
    # Run forecasts
    if args.methods:
        print(f"\nRunning methods: {', '.join(args.methods)}")
        for method in args.methods:
            print(f"\nRunning {method}...")
            getattr(engine, f'forecast_{method.lower()}')()
    else:
        print("\nRunning all available methods...")
        engine.run_all_forecasts()
    
    # Display results
    if engine.metrics:
        print("\n" + "=" * 60)
        print("PERFORMANCE METRICS")
        print("=" * 60)
        print(engine.get_metrics_summary())
        
        best_model, metrics = engine.get_best_model()
        print(f"\n🏆 Best Model: {best_model}")
        print(f"   MAE: {metrics['MAE']:.3f}")
        print(f"   RMSE: {metrics['RMSE']:.3f}")
        print(f"   MAPE: {metrics['MAPE']:.2f}%")
    
    # Export results
    engine.export_results(args.output)
    
    # Create plot
    plot_forecasts(engine, args.plot)
    
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
