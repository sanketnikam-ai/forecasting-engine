# 🚀 GETTING STARTED - Choose Your Path

## Path 1: Web Application (Recommended for Most Users)

### ✨ What You Get
- Beautiful web interface
- Drag & drop file upload
- Visual charts and metrics
- No coding required
- Share with others online

### 🎯 Quick Deploy (5 minutes)

#### Option A: Render.com (FREE & Easiest)
1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect this GitHub repo
4. Click "Create Web Service"
5. ✅ Done! You get a URL like: `https://your-app.onrender.com`

#### Option B: Heroku (FREE tier)
```bash
# Install Heroku CLI first
heroku create your-app-name
git push heroku main
heroku open
```

#### Option C: Run Locally
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements_web.txt

# Run app
python app.py

# Open browser to http://localhost:5000
```

#### Option D: Docker (if you have Docker installed)
```bash
# Easy way - use the build script
./build.sh

# Or manually
docker build -t forecasting-engine .
docker run -p 5000:5000 forecasting-engine

# Or with Docker Compose
docker-compose up -d
```

**Having Docker issues?** See `DOCKER_TROUBLESHOOTING.md` or skip Docker and use Render.com instead!

### 📖 Full Web Guide
See **README_WEB.md** and **DEPLOYMENT.md** for detailed instructions

---

## Path 2: Python Script (For Developers/Analysts)

### ✨ What You Get
- Full programmatic control
- Run in Jupyter notebooks
- Batch processing
- Integration into existing workflows

### 🎯 Quick Start

```python
from forecasting_engine import ForecastingEngine

# Load your data
engine = ForecastingEngine('your_data.csv')

# Split train/test
engine.split_data(test_size=0.2)

# Run all methods
engine.run_all_forecasts()

# See results
print(engine.get_metrics_summary())
best_model, metrics = engine.get_best_model()
print(f"Best: {best_model} - MAPE: {metrics['MAPE']:.2f}%")

# Export
engine.export_results('results.csv')
```

### 📖 Full Script Guide
See **README.md** and **QUICKSTART.md** for detailed instructions

---

## Path 3: Command Line Interface

### ✨ What You Get
- Simple command-line tool
- Quick forecasting
- Scriptable
- No web server needed

### 🎯 Quick Start

```bash
# Basic usage
python forecast_cli.py your_data.csv

# With options
python forecast_cli.py your_data.csv \
  --date-col "Date" \
  --value-col "Sales" \
  --test-size 20 \
  --methods SARIMA Prophet XGBoost
```

### 📖 Full CLI Guide
See **README.md** for all options

---

## 📂 What's Included

### Core Files
- `forecasting_engine.py` - Main forecasting engine (all 6 methods)
- `requirements.txt` - Python dependencies

### Web Application
- `app.py` - Flask web server
- `templates/index.html` - Web interface
- `static/css/style.css` - Styling
- `static/js/app.js` - Frontend logic
- `requirements_web.txt` - Web dependencies

### Deployment
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Docker orchestration
- `Procfile` - Heroku deployment
- `render.yaml` - Render.com deployment
- `nginx.conf` - Production web server config
- `setup.sh` - VPS setup script

### Documentation
- `README.md` - Python script documentation
- `README_WEB.md` - Web app documentation
- `DEPLOYMENT.md` - Complete hosting guide
- `QUICKSTART.md` - 3-step quick start
- `forecasting_tutorial.ipynb` - Jupyter tutorial

### Sample Data
- `sample_data.csv` - Test data

---

## 🎯 Recommended Path

### For Non-Programmers
→ **Web Application** on Render.com (free, 5 minutes)

### For Data Scientists
→ **Python Script** or Jupyter Notebook

### For DevOps/Production
→ **Web Application** on AWS/GCP with Docker

### For Quick Analysis
→ **Command Line** interface

---

## 📊 Method Comparison

| Method | Best For | Speed | Accuracy | Complexity |
|--------|----------|-------|----------|------------|
| SARIMA | Clear seasonality | Medium | High | Medium |
| Holt-Winters | Simple patterns | Fast | Good | Low |
| TBATS | Multiple seasons | Slow | High | Medium |
| Prophet | Daily + holidays | Medium | Good | Low |
| XGBoost | Complex patterns | Fast | High | Medium |
| TFT | Large datasets | Very Slow | Highest | High |

**Quick Tip**: Start with SARIMA, Prophet, and XGBoost. They cover most use cases!

---

## 🆘 Common Questions

### Q: Which hosting is best?
**A**: For beginners: Render.com (free). For production: AWS/GCP.

### Q: How much data do I need?
**A**: Minimum 30 points, ideally 100+ for best results.

### Q: Which method should I use?
**A**: Run all methods and compare! The engine shows you the best performer.

### Q: Can I use this for production?
**A**: Yes! Deploy on AWS/GCP, add authentication, monitoring.

### Q: Is it really free?
**A**: Yes! The code is MIT licensed. Some cloud platforms have free tiers.

---

## 🚀 Next Steps

1. **Choose your path** from above
2. **Follow the guide** for that path
3. **Test with sample data** (sample_data.csv)
4. **Upload your own data**
5. **Get forecasts!**

---

## 📞 Need Help?

1. Check the relevant README for your path
2. Review DEPLOYMENT.md for hosting issues
3. Try the sample data first
4. Check error messages carefully

---

## ✅ Quick Health Check

After setup, verify everything works:

### Web App
- Visit your URL
- Upload sample_data.csv
- Run forecast with 2-3 methods
- Check you get results

### Python Script
```python
from forecasting_engine import create_sample_data, ForecastingEngine
df = create_sample_data()
engine = ForecastingEngine(df=df)
engine.split_data()
engine.forecast_prophet()
print(engine.metrics)
```

---

**Ready to start? Pick your path above!** 🎉

For detailed guides:
- Web App → **README_WEB.md** + **DEPLOYMENT.md**
- Python → **README.md** + **QUICKSTART.md**
- Tutorial → **forecasting_tutorial.ipynb**
