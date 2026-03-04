# 🚀 QUICK REFERENCE - Forecasting Engine

## Fastest Deployment (No Docker, No Setup) ⚡

### Render.com - 5 Minutes, 100% Free
1. Go to https://render.com
2. Sign up (free, no credit card)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Click "Create Web Service"
6. ✅ Done! Get URL like: `https://your-app.onrender.com`

**This is the recommended option if you just want it online fast!**

---

## Local Testing 💻

```bash
# Install
pip install -r requirements.txt -r requirements_web.txt

# Run
python app.py

# Visit
http://localhost:5000
```

---

## Docker Commands 🐳

```bash
# Build
./build.sh
# OR
docker build -t forecasting-engine .

# Run
docker run -p 5000:5000 forecasting-engine

# With Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Docker not working?** Use Render.com instead!

---

## File Structure 📁

```
your-project/
├── app.py                    # Web server
├── forecasting_engine.py     # Core engine
├── requirements.txt          # Dependencies
├── requirements_web.txt      # Web dependencies
├── Dockerfile               # Container config
├── docker-compose.yml       # Docker orchestration
├── static/                  # CSS & JS
│   ├── css/style.css
│   └── js/app.js
└── templates/               # HTML
    └── index.html
```

---

## Python Usage 🐍

```python
from forecasting_engine import ForecastingEngine

# Load data
engine = ForecastingEngine('data.csv')

# Split train/test
engine.split_data(test_size=0.2)

# Run forecasts
engine.run_all_forecasts()

# Get results
print(engine.get_metrics_summary())
best, metrics = engine.get_best_model()
```

---

## CLI Usage 💻

```bash
# Basic
python forecast_cli.py data.csv

# With options
python forecast_cli.py data.csv \
  --date-col "Date" \
  --value-col "Sales" \
  --test-size 20 \
  --methods SARIMA Prophet XGBoost
```

---

## Common Issues & Fixes 🔧

### Issue: Docker build fails
**Fix**: Use Render.com (no Docker needed) or see `DOCKER_TROUBLESHOOTING.md`

### Issue: Module not found
**Fix**: `pip install -r requirements.txt -r requirements_web.txt`

### Issue: Port already in use
**Fix**: Use different port: `python app.py --port 8000`

### Issue: Upload fails
**Fix**: Check CSV has date + value columns

---

## Hosting Costs 💰

| Platform | Cost | Setup |
|----------|------|-------|
| Render.com | FREE | 5 min |
| Heroku | FREE tier | 10 min |
| Railway | $5 credit | 5 min |
| VPS | $2.50+/mo | 30 min |

---

## Methods Comparison 📊

| Method | Speed | Use For |
|--------|-------|---------|
| SARIMA | Medium | Seasonality |
| Holt-Winters | Fast | Simple trends |
| TBATS | Slow | Multiple seasons |
| Prophet | Medium | Daily + holidays |
| XGBoost | Fast | Complex patterns |
| TFT | Very Slow | Large datasets |

**Recommended**: Start with SARIMA, Prophet, XGBoost

---

## Support Files 📚

- `GETTING_STARTED.md` - Choose your deployment path
- `DEPLOYMENT.md` - Detailed hosting guide (8 options)
- `DOCKER_TROUBLESHOOTING.md` - Fix Docker issues
- `README.md` - Python API documentation
- `README_WEB.md` - Web app documentation
- `forecasting_tutorial.ipynb` - Jupyter tutorial

---

## Quick Health Check ✅

After deployment, test:

1. Visit your URL
2. Upload `sample_data.csv`
3. Select: date, value columns
4. Choose 2-3 methods
5. Click "Run Forecast"
6. Should see results in 1-2 minutes

---

## One-Line Deployments 🚀

### Render.com
```
Click "New Web Service" → Connect Repo → Deploy
```

### Heroku
```bash
heroku create && git push heroku main
```

### Railway
```
Connect GitHub → Auto-deploy
```

### Local
```bash
pip install -r requirements.txt -r requirements_web.txt && python app.py
```

---

## Emergency: Nothing Works? 🆘

1. **Skip Docker** - Use Render.com (handles everything)
2. **Run Locally** - `python app.py`
3. **Check Logs** - Error messages tell you what's wrong
4. **Read** - `DOCKER_TROUBLESHOOTING.md`

**Seriously, just use Render.com - it's free and takes 5 minutes!**

---

## Success Checklist ✓

- [ ] All files downloaded
- [ ] Dependencies installed OR using Render.com
- [ ] App running (locally or online)
- [ ] Can upload CSV
- [ ] Can run forecast
- [ ] Can download results

If all checked: **You're done!** 🎉

---

**Need help?** Check the detailed guides:
- New to this? → `GETTING_STARTED.md`
- Docker issues? → `DOCKER_TROUBLESHOOTING.md`
- Deployment? → `DEPLOYMENT.md`
