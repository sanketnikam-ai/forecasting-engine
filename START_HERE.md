# 📈 Forecasting Engine - Complete Package

A comprehensive time series forecasting system with 6 methods, beautiful web interface, and multiple deployment options.

---

## 🎯 QUICK START (Choose One Path)

### ⭐ Path 1: Deploy Online in 5 Minutes (RECOMMENDED)
**Use Render.com - Free, No Credit Card, No Docker Knowledge Needed**

1. Upload this folder to GitHub
2. Go to https://render.com and sign up (free)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. ✅ Done! Your app is live

📖 **Full guide:** `NO_DOCKER_DEPLOY.md`

---

### 💻 Path 2: Run Locally (Testing)

```bash
# Install dependencies
pip install -r requirements.txt -r requirements_web.txt

# Run the app
python app_standalone.py

# Open browser
http://localhost:5000
```

---

### 🐳 Path 3: Docker (If You Must)

```bash
# Option A: Use standalone version (recommended)
docker build -f Dockerfile.standalone -t forecasting-engine .
docker run -p 5000:5000 forecasting-engine

# Option B: Use build script
./build.sh

# Option C: Use docker-compose
docker-compose up -d
```

📖 **Having Docker issues?** See `DOCKER_TROUBLESHOOTING.md`

---

### 🐍 Path 4: Python Script/API

```python
from forecasting_engine import ForecastingEngine

# Load data
engine = ForecastingEngine('your_data.csv')
engine.split_data(test_size=0.2)

# Run forecasts
engine.run_all_forecasts()

# Get results
print(engine.get_metrics_summary())
```

📖 **Full guide:** `README.md` and `QUICKSTART.md`

---

## 📦 What's Included

### Core Files
- `forecasting_engine.py` - Main forecasting engine (6 methods)
- `app.py` - Flask web application
- `app_standalone.py` - Single-file web app (no directories needed)
- `forecast_cli.py` - Command-line interface

### Web Interface
- `templates/index.html` - Web UI
- `static/css/style.css` - Styling
- `static/js/app.js` - Frontend logic

### Deployment Configs
- `Dockerfile` - Standard Docker config
- `Dockerfile.simple` - Simplified Docker
- `Dockerfile.standalone` - Standalone app Docker (RECOMMENDED)
- `docker-compose.yml` - Docker Compose
- `Procfile` - Heroku deployment
- `render.yaml` - Render.com deployment
- `nginx.conf` - Production web server

### Documentation
- `GETTING_STARTED.md` - Choose your path
- `NO_DOCKER_DEPLOY.md` - Deploy without Docker (6 methods)
- `DEPLOYMENT.md` - Complete hosting guide (8 platforms)
- `DOCKER_TROUBLESHOOTING.md` - Fix Docker issues
- `QUICK_REFERENCE.md` - One-page cheat sheet
- `README.md` - Python API docs
- `README_WEB.md` - Web app docs
- `QUICKSTART.md` - 3-step quick start

### Helpers
- `build.sh` - Automated Docker build
- `setup.sh` - VPS setup script
- `sample_data.csv` - Test data
- `forecasting_tutorial.ipynb` - Jupyter tutorial

---

## 🌟 Features

### 6 Forecasting Methods
1. **SARIMA** - Seasonal patterns
2. **Holt-Winters** - Trend + seasonality
3. **TBATS** - Complex seasonality
4. **Prophet** - Daily data with holidays
5. **XGBoost** - Machine learning
6. **TFT** - Deep learning (optional)

### Web Interface
- Drag & drop CSV upload
- Interactive configuration
- Visual charts and metrics
- Performance comparison
- Export results

### Multiple Deployment Options
- Render.com (FREE)
- Heroku
- Railway
- AWS/GCP/Azure
- DigitalOcean
- Any VPS
- Docker
- Local

---

## 📊 Quick Examples

### Web Interface
1. Open http://localhost:5000 (or your deployed URL)
2. Upload `sample_data.csv`
3. Select columns and methods
4. Click "Run Forecast"
5. View results and download

### Python API
```python
from forecasting_engine import ForecastingEngine

# Initialize
engine = ForecastingEngine('data.csv', date_col='date', value_col='value')
engine.split_data(test_size=0.2)

# Run specific method
engine.forecast_prophet()

# Or run all methods
engine.run_all_forecasts()

# Get best model
best, metrics = engine.get_best_model()
print(f"Best: {best}, MAPE: {metrics['MAPE']:.2f}%")
```

### Command Line
```bash
# Basic
python forecast_cli.py data.csv

# Advanced
python forecast_cli.py data.csv \
  --date-col "Date" \
  --value-col "Sales" \
  --methods SARIMA Prophet XGBoost \
  --test-size 20
```

---

## 🎯 Recommended Deployment Path

### For Beginners
1. **Use Render.com** (see `NO_DOCKER_DEPLOY.md`)
   - Free, 5 minutes
   - No Docker knowledge needed
   - Just works

### For Developers
1. Test locally: `python app_standalone.py`
2. Deploy to Render/Heroku when ready

### For Production
1. Use Docker on AWS/GCP
2. Setup monitoring and auto-scaling
3. Add authentication

---

## 🔧 Requirements

### Python Packages
```
pandas, numpy, scikit-learn
statsmodels (SARIMA, Holt-Winters)
prophet (Prophet)
xgboost (XGBoost)
tbats (TBATS)
Flask, gunicorn (Web app)
matplotlib, seaborn (Visualization)
```

All specified in `requirements.txt` and `requirements_web.txt`

### System Requirements
- Python 3.8+
- 2GB RAM minimum (4GB recommended)
- Works on Windows, Mac, Linux

---

## 📖 Documentation Guide

**Start here:**
- `GETTING_STARTED.md` - Overview of all paths

**For web deployment:**
- `NO_DOCKER_DEPLOY.md` - 6 ways without Docker
- `DEPLOYMENT.md` - 8 hosting platforms
- `README_WEB.md` - Web app documentation

**For Python usage:**
- `README.md` - Full API documentation
- `QUICKSTART.md` - 3-step quick start
- `forecasting_tutorial.ipynb` - Jupyter tutorial

**For troubleshooting:**
- `DOCKER_TROUBLESHOOTING.md` - Fix Docker issues
- `QUICK_REFERENCE.md` - Common commands

---

## 🆘 Having Issues?

### Docker build fails
→ See `DOCKER_TROUBLESHOOTING.md`
→ Or skip Docker and use `NO_DOCKER_DEPLOY.md`

### Module not found
```bash
pip install -r requirements.txt -r requirements_web.txt
```

### Port already in use
```bash
# Change port
python app_standalone.py --port 8000
```

### Best solution: Use Render.com!
No Docker, no setup, just works. See `NO_DOCKER_DEPLOY.md`

---

## 💰 Hosting Costs

| Platform | Free Tier | Paid From | Best For |
|----------|-----------|-----------|----------|
| Render.com | ✅ Yes | $7/mo | Getting started |
| Heroku | Limited | $5/mo | Quick deploy |
| Railway | $5 credit | Usage-based | Developers |
| PythonAnywhere | ✅ Yes | $5/mo | Beginners |
| VPS (Vultr/Linode) | No | $2.50/mo | Full control |
| AWS/GCP | Free tier | Usage-based | Production |

**Recommendation: Start with Render.com (free)**

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Can access the web interface
- [ ] Can upload CSV file
- [ ] Can select columns
- [ ] Can run forecast
- [ ] See results and charts
- [ ] Can download results CSV

Test with `sample_data.csv` first!

---

## 🎓 Learn More

- **Jupyter Tutorial**: Open `forecasting_tutorial.ipynb`
- **API Examples**: See `README.md`
- **Web Examples**: See `README_WEB.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`

---

## 📄 License

MIT License - Free to use for any purpose, commercial or personal.

---

## 🚀 Ready to Start?

1. **Choose your path** (see QUICK START above)
2. **Follow the guide** for that path
3. **Test with sample data**
4. **Deploy your forecasts!**

**Recommended:** Check `GETTING_STARTED.md` for detailed path selection.

**Easiest:** Use Render.com (see `NO_DOCKER_DEPLOY.md`)

---

## 📞 Quick Links

- 🌐 [Render.com](https://render.com) - Free hosting
- 🐙 [GitHub](https://github.com) - Code hosting
- 📊 [Upload your CSV] - After deployment
- 📈 [Get forecasts] - In minutes!

---

**Questions? Check the relevant guide in the documentation!**

Everything you need is included. Just pick your path and go! 🎉
