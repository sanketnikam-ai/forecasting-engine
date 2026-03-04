"""
Flask Web Application for Forecasting Engine
Allows users to upload CSV files and get forecasts via web interface
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
import json
from datetime import datetime
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from forecasting_engine import ForecastingEngine

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and preview"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read and preview data
        try:
            df = pd.read_csv(filepath)
            preview = {
                'filename': filename,
                'rows': len(df),
                'columns': df.columns.tolist(),
                'preview': df.head(10).to_dict('records'),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
            return jsonify(preview)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
    
    return jsonify({'error': 'Invalid file type. Only CSV allowed'}), 400


@app.route('/api/forecast', methods=['POST'])
def run_forecast():
    """Run forecasting"""
    try:
        data = request.json
        filename = data.get('filename')
        date_col = data.get('date_col', 'date')
        value_col = data.get('value_col', 'value')
        freq = data.get('freq', 'D')
        test_size = float(data.get('test_size', 0.2))
        methods = data.get('methods', [])
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Initialize engine
        engine = ForecastingEngine(
            data_path=filepath,
            date_col=date_col,
            value_col=value_col,
            freq=freq
        )
        
        # Split data
        engine.split_data(test_size=test_size)
        
        # Run forecasts
        if methods and len(methods) > 0:
            for method in methods:
                method_func = getattr(engine, f'forecast_{method.lower()}', None)
                if method_func:
                    method_func()
        else:
            engine.run_all_forecasts()
        
        # Get results
        metrics = engine.get_metrics_summary()
        
        # Create plot
        plot_path = os.path.join(app.config['RESULTS_FOLDER'], f"{filename}_plot.png")
        create_forecast_plot(engine, plot_path)
        
        # Convert plot to base64
        with open(plot_path, 'rb') as f:
            plot_data = base64.b64encode(f.read()).decode()
        
        # Export results
        results_path = os.path.join(app.config['RESULTS_FOLDER'], f"{filename}_results.csv")
        engine.export_results(results_path)
        
        # Get best model
        best_model, best_metrics = engine.get_best_model()
        
        response = {
            'success': True,
            'metrics': metrics.to_dict(),
            'best_model': best_model,
            'best_metrics': best_metrics,
            'plot': f'data:image/png;base64,{plot_data}',
            'results_file': f"{filename}_results.csv",
            'train_size': len(engine.train),
            'test_size': len(engine.test)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_results(filename):
    """Download results CSV"""
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


def create_forecast_plot(engine, save_path):
    """Create forecast visualization"""
    plt.figure(figsize=(15, 8))
    
    # Plot training data
    plt.plot(engine.train.index, engine.train[engine.value_col], 
             label='Train', color='black', linewidth=2, alpha=0.7)
    
    # Plot actual test data
    plt.plot(engine.test.index, engine.test[engine.value_col], 
             label='Actual', color='blue', linewidth=2.5)
    
    # Plot forecasts
    colors = ['red', 'green', 'orange', 'purple', 'brown', 'pink']
    for i, (method, result) in enumerate(engine.results.items()):
        forecast = result['forecast']
        plt.plot(engine.test.index[:len(forecast)], forecast,
                 label=method, color=colors[i % len(colors)], 
                 linestyle='--', linewidth=2, alpha=0.8)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.title('Forecasting Methods Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
