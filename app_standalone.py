"""
Single-File Flask Application for Forecasting Engine
No external static/templates needed - everything embedded
"""

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from forecasting_engine import ForecastingEngine

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

# Embedded HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forecasting Engine</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding: 30px 0;
        }
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .subtitle { font-size: 1.2em; opacity: 0.9; }
        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 8px;
            padding: 50px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover { background: #f8f9ff; border-color: #764ba2; }
        .form-group { margin-bottom: 20px; }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 1em;
        }
        .form-control:focus { outline: none; border-color: #667eea; }
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 6px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        .btn-secondary {
            background: #28a745;
            color: white;
        }
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        .checkbox-group label {
            display: flex;
            align-items: center;
            padding: 10px;
            background: #f8f9ff;
            border-radius: 6px;
            cursor: pointer;
        }
        .checkbox-group input { margin-right: 8px; }
        .results-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
        }
        .stat-label { font-size: 0.9em; opacity: 0.9; margin-bottom: 8px; }
        .stat-value { font-size: 1.8em; font-weight: bold; }
        .plot-container { margin: 30px 0; text-align: center; }
        .plot-container img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin-top: 15px;
        }
        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        tbody tr:hover { background: #f8f9ff; }
        tbody tr.best-model { background: #e8f5e9; font-weight: bold; }
        #loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        #loading-overlay p { color: white; font-size: 1.2em; margin-top: 20px; }
        .spinner {
            width: 60px;
            height: 60px;
            border: 6px solid rgba(255, 255, 255, 0.3);
            border-top: 6px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        footer {
            text-align: center;
            color: white;
            padding: 20px;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📈 Forecasting Engine</h1>
            <p class="subtitle">Multi-Method Time Series Forecasting</p>
        </header>

        <div class="card" id="upload-section">
            <h2>Step 1: Upload Your Data</h2>
            <div class="upload-area" id="upload-area">
                <input type="file" id="file-input" accept=".csv" style="display: none;">
                <div class="upload-content">
                    <p style="font-size: 3em;">📁</p>
                    <p style="margin: 10px 0; font-size: 1.1em;">Click to upload or drag & drop</p>
                    <p style="color: #666; font-size: 0.9em;">CSV files only (max 16MB)</p>
                </div>
            </div>
            <div id="file-info" style="display: none; margin-top: 20px; padding: 20px; background: #f8f9ff; border-radius: 8px;"></div>
        </div>

        <div class="card" id="config-section" style="display: none;">
            <h2>Step 2: Configure Forecast</h2>
            <div class="form-group">
                <label for="date-col">Date Column:</label>
                <select id="date-col" class="form-control"></select>
            </div>
            <div class="form-group">
                <label for="value-col">Value Column:</label>
                <select id="value-col" class="form-control"></select>
            </div>
            <div class="form-group">
                <label for="freq">Frequency:</label>
                <select id="freq" class="form-control">
                    <option value="D">Daily</option>
                    <option value="W">Weekly</option>
                    <option value="M">Monthly</option>
                </select>
            </div>
            <div class="form-group">
                <label for="test-size">Test Size (%):</label>
                <input type="number" id="test-size" class="form-control" value="20" min="10" max="50">
            </div>
            <div class="form-group">
                <label>Forecasting Methods:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" value="SARIMA" checked> SARIMA</label>
                    <label><input type="checkbox" value="HoltWinters" checked> Holt-Winters</label>
                    <label><input type="checkbox" value="Prophet" checked> Prophet</label>
                    <label><input type="checkbox" value="XGBoost" checked> XGBoost</label>
                </div>
            </div>
            <button id="run-forecast" class="btn btn-primary">Run Forecast</button>
        </div>

        <div class="card" id="results-section" style="display: none;">
            <h2>Step 3: Results</h2>
            <div class="results-summary">
                <div class="stat-card">
                    <div class="stat-label">Best Model</div>
                    <div class="stat-value" id="best-model">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">MAPE</div>
                    <div class="stat-value" id="best-mape">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Train Size</div>
                    <div class="stat-value" id="train-size">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Test Size</div>
                    <div class="stat-value" id="test-size-display">-</div>
                </div>
            </div>
            <div class="plot-container">
                <img id="forecast-plot" src="" alt="Forecast Plot" style="display: none;">
            </div>
            <div class="metrics-table">
                <h3>Performance Metrics</h3>
                <table id="metrics-table">
                    <thead>
                        <tr>
                            <th>Method</th>
                            <th>MAE</th>
                            <th>RMSE</th>
                            <th>MAPE (%)</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
            <button id="download-results" class="btn btn-secondary" style="margin-top: 20px;">Download Results CSV</button>
        </div>

        <div id="loading-overlay" style="display: none;">
            <div class="spinner"></div>
            <p>Running forecasts... This may take a few minutes.</p>
        </div>
    </div>

    <footer>
        <p>Forecasting Engine v1.0 | Supports SARIMA, Holt-Winters, Prophet, XGBoost</p>
    </footer>

    <script>
        let currentFilename = null;
        let currentColumns = [];

        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');

        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.style.background = '#f0f4ff'; });
        uploadArea.addEventListener('dragleave', () => { uploadArea.style.background = ''; });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.background = '';
            if (e.dataTransfer.files.length > 0) handleFileUpload(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) handleFileUpload(e.target.files[0]);
        });

        async function handleFileUpload(file) {
            if (!file.name.endsWith('.csv')) { alert('Please upload a CSV file'); return; }
            const formData = new FormData();
            formData.append('file', file);
            showLoading();
            try {
                const response = await fetch('/api/upload', { method: 'POST', body: formData });
                const data = await response.json();
                hideLoading();
                if (response.ok) {
                    currentFilename = data.filename;
                    currentColumns = data.columns;
                    displayFileInfo(data);
                    showConfigSection();
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                hideLoading();
                alert('Upload failed: ' + error.message);
            }
        }

        function displayFileInfo(data) {
            const fileInfo = document.getElementById('file-info');
            fileInfo.style.display = 'block';
            fileInfo.innerHTML = `
                <h3 style="color: #667eea; margin-bottom: 10px;">📄 File Uploaded Successfully</h3>
                <p><strong>Rows:</strong> ${data.rows.toLocaleString()}</p>
                <p><strong>Columns:</strong> ${data.columns.join(', ')}</p>
            `;
        }

        function showConfigSection() {
            document.getElementById('config-section').style.display = 'block';
            const dateCol = document.getElementById('date-col');
            const valueCol = document.getElementById('value-col');
            dateCol.innerHTML = '';
            valueCol.innerHTML = '';
            currentColumns.forEach(col => {
                dateCol.innerHTML += `<option value="${col}">${col}</option>`;
                valueCol.innerHTML += `<option value="${col}">${col}</option>`;
            });
            const dateLike = currentColumns.filter(col => col.toLowerCase().includes('date') || col.toLowerCase().includes('time'));
            if (dateLike.length > 0) dateCol.value = dateLike[0];
            const valueLike = currentColumns.filter(col => col.toLowerCase().includes('value') || col.toLowerCase().includes('sales') || col.toLowerCase().includes('price'));
            if (valueLike.length > 0) valueCol.value = valueLike[0];
            else if (currentColumns.length > 1) valueCol.value = currentColumns[1];
        }

        document.getElementById('run-forecast').addEventListener('click', async () => {
            const methods = Array.from(document.querySelectorAll('.checkbox-group input:checked')).map(cb => cb.value);
            if (methods.length === 0) { alert('Please select at least one method'); return; }
            const requestData = {
                filename: currentFilename,
                date_col: document.getElementById('date-col').value,
                value_col: document.getElementById('value-col').value,
                freq: document.getElementById('freq').value,
                test_size: document.getElementById('test-size').value / 100,
                methods: methods
            };
            showLoading();
            try {
                const response = await fetch('/api/forecast', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });
                const data = await response.json();
                hideLoading();
                if (response.ok) displayResults(data);
                else alert('Forecast failed: ' + data.error);
            } catch (error) {
                hideLoading();
                alert('Request failed: ' + error.message);
            }
        });

        function displayResults(data) {
            document.getElementById('results-section').style.display = 'block';
            document.getElementById('best-model').textContent = data.best_model;
            document.getElementById('best-mape').textContent = data.best_metrics.MAPE.toFixed(2) + '%';
            document.getElementById('train-size').textContent = data.train_size.toLocaleString();
            document.getElementById('test-size-display').textContent = data.test_size.toLocaleString();
            const plotImg = document.getElementById('forecast-plot');
            plotImg.src = data.plot;
            plotImg.style.display = 'block';
            const tableBody = document.querySelector('#metrics-table tbody');
            tableBody.innerHTML = '';
            const metrics = data.metrics;
            Object.keys(metrics).sort((a, b) => metrics[a].MAPE - metrics[b].MAPE).forEach(method => {
                const row = document.createElement('tr');
                if (method === data.best_model) row.classList.add('best-model');
                row.innerHTML = `
                    <td>${method} ${method === data.best_model ? '🏆' : ''}</td>
                    <td>${metrics[method].MAE.toFixed(3)}</td>
                    <td>${metrics[method].RMSE.toFixed(3)}</td>
                    <td>${metrics[method].MAPE.toFixed(2)}%</td>
                `;
                tableBody.appendChild(row);
            });
            document.getElementById('download-results').onclick = () => {
                window.location.href = `/api/download/${data.results_file}`;
            };
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
        }

        function showLoading() { document.getElementById('loading-overlay').style.display = 'flex'; }
        function hideLoading() { document.getElementById('loading-overlay').style.display = 'none'; }
    </script>
</body>
</html>"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/upload', methods=['POST'])
def upload_file():
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
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/forecast', methods=['POST'])
def run_forecast():
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
        
        engine = ForecastingEngine(
            data_path=filepath,
            date_col=date_col,
            value_col=value_col,
            freq=freq
        )
        
        engine.split_data(test_size=test_size)
        
        if methods and len(methods) > 0:
            for method in methods:
                method_func = getattr(engine, f'forecast_{method.lower()}', None)
                if method_func:
                    method_func()
        else:
            engine.run_all_forecasts()
        
        metrics = engine.get_metrics_summary()
        plot_path = os.path.join(app.config['RESULTS_FOLDER'], f"{filename}_plot.png")
        create_forecast_plot(engine, plot_path)
        
        with open(plot_path, 'rb') as f:
            plot_data = base64.b64encode(f.read()).decode()
        
        results_path = os.path.join(app.config['RESULTS_FOLDER'], f"{filename}_results.csv")
        engine.export_results(results_path)
        
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
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

def create_forecast_plot(engine, save_path):
    plt.figure(figsize=(15, 8))
    plt.plot(engine.train.index, engine.train[engine.value_col], 
             label='Train', color='black', linewidth=2, alpha=0.7)
    plt.plot(engine.test.index, engine.test[engine.value_col], 
             label='Actual', color='blue', linewidth=2.5)
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
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
