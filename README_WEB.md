# Forecasting Engine - Web Application

A beautiful web interface for multi-method time series forecasting. Upload CSV files and get instant forecasts using 6 different methods.

## 🌟 Features

- **Web Interface**: Beautiful, responsive UI
- **Drag & Drop**: Easy file upload
- **6 Forecasting Methods**: SARIMA, Holt-Winters, TBATS, Prophet, XGBoost, TFT
- **Visual Results**: Interactive charts and performance metrics
- **Export Results**: Download forecasts as CSV
- **Mobile Friendly**: Works on all devices

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements_web.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Browser
Visit `http://localhost:5000`

## 📦 Deploy to Cloud

### Fastest: Render.com (FREE)
1. Fork this repository
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Click "Create Web Service"
6. Done! Your app is live

### Docker Deployment
```bash
# Build
docker build -t forecasting-engine .

# Run
docker run -p 5000:5000 forecasting-engine

# Or use Docker Compose
docker-compose up -d
```

## 🎯 How to Use

### Step 1: Upload Data
- Click upload area or drag & drop CSV file
- File must have date and value columns

### Step 2: Configure
- Select date column
- Select value column
- Choose frequency (Daily, Weekly, Monthly)
- Set test size (% of data for validation)
- Select forecasting methods

### Step 3: Run Forecast
- Click "Run Forecast"
- Wait for results (1-5 minutes depending on methods)

### Step 4: View Results
- See performance metrics
- View forecast plots
- Download results CSV

## 📊 CSV Format

Your CSV should look like this:

```csv
date,value
2023-01-01,100
2023-01-02,105
2023-01-03,110
...
```

Column names can be anything, you'll select them in the interface.

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production  # For production deployment
PORT=5000            # Port to run on (auto-set by cloud platforms)
```

### File Upload Limits
Default: 16MB (configured in app.py)

To change:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

## 🌐 API Endpoints

If you want to use the API directly:

### Upload File
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@your_data.csv"
```

### Run Forecast
```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "uploaded_file.csv",
    "date_col": "date",
    "value_col": "value",
    "freq": "D",
    "test_size": 0.2,
    "methods": ["SARIMA", "Prophet", "XGBoost"]
  }'
```

### Download Results
```bash
curl -O http://localhost:5000/api/download/results.csv
```

## 📁 Project Structure

```
forecasting-engine/
├── app.py                    # Flask application
├── forecasting_engine.py     # Core forecasting logic
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── css/style.css        # Styles
│   └── js/app.js            # Frontend logic
├── requirements.txt         # Python dependencies
├── requirements_web.txt     # Web dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose config
└── DEPLOYMENT.md           # Deployment guide
```

## 🐛 Troubleshooting

### App won't start
- Check all dependencies installed
- Verify Python version (3.8+)
- Check port 5000 is available

### File upload fails
- Check file is valid CSV
- File size under 16MB
- Columns contain date and numeric values

### Forecast fails
- Ensure date column is valid dates
- Value column must be numeric
- Need at least 30 data points
- Some methods need more data

### Slow performance
- TFT is very slow (disable for faster results)
- Larger datasets take longer
- Consider upgrading server resources

## 🔐 Security Notes

For production deployment:
- Enable HTTPS (automatic on most cloud platforms)
- Set strong SECRET_KEY in environment variables
- Implement rate limiting for API endpoints
- Regular security updates

## 📈 Performance Tips

### Faster Forecasts
- Disable TFT (very slow)
- Use fewer methods
- Smaller test size
- Reduce data size for initial testing

### Better Accuracy
- More historical data
- Clean your data (no gaps/outliers)
- Match frequency to your data
- Try all methods and compare

## 🎨 Customization

### Change Theme Colors
Edit `static/css/style.css`:
```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #yourcolor1 0%, #yourcolor2 100%);
```

### Add Logo
Add image to `static/` folder and update `templates/index.html`:
```html
<header>
    <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo">
    <h1>Your Company</h1>
</header>
```

## 📞 Support

For issues:
1. Check DEPLOYMENT.md for hosting issues
2. Check TROUBLESHOOTING section above
3. Review logs: `docker-compose logs -f`

## 📄 License

MIT License - Free to use for any purpose

## 🙏 Credits

Built with:
- Flask (Web framework)
- statsmodels, prophet, xgboost (Forecasting)
- Chart.js (Visualization)
- Modern CSS/JavaScript

---

**Ready to deploy?** Check out `DEPLOYMENT.md` for detailed hosting instructions! 🚀
