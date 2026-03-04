# Deployment Guide - Forecasting Engine

This guide covers multiple hosting options from free to enterprise-level.

---

## 🚀 Quick Deployment Options

### Option 1: Render.com (FREE - Easiest)
**Best for**: Quick deployment, no credit card required

**Steps:**
1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render auto-detects the `render.yaml` configuration
5. Click "Create Web Service"
6. Your app will be live at `https://your-app-name.onrender.com`

**Pros**: Free tier, easy setup, automatic HTTPS
**Cons**: Spins down after inactivity (slow cold starts)

---

### Option 2: Heroku (FREE tier available)
**Best for**: Reliable hosting with good documentation

**Steps:**
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

**Pros**: Reliable, good free tier, easy scaling
**Cons**: Requires credit card for free tier

---

### Option 3: Railway.app (FREE $5 credit)
**Best for**: Developer-friendly deployment

**Steps:**
1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-deploys
5. Get your URL from the deployments tab

**Pros**: Easy deployment, generous free tier
**Cons**: Limited free credits

---

### Option 4: Google Cloud Run (Serverless)
**Best for**: Pay-per-use, scales to zero

**Steps:**
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/forecasting-engine
gcloud run deploy forecasting-engine \
  --image gcr.io/YOUR_PROJECT_ID/forecasting-engine \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Pros**: Scales automatically, pay only when used
**Cons**: Requires GCP account and credit card

---

### Option 5: AWS (EC2 + Docker)
**Best for**: Full control, production workloads

**Steps:**

1. **Launch EC2 Instance**
   - Go to AWS Console → EC2
   - Launch Ubuntu 22.04 instance (t2.medium recommended)
   - Configure security group: Allow ports 22, 80, 443

2. **Connect to instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Docker**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

4. **Deploy application**
```bash
# Clone your repository
git clone https://github.com/your-repo/forecasting-engine.git
cd forecasting-engine

# Build and run
docker-compose up -d

# Check status
docker-compose ps
```

5. **Setup Nginx (optional)**
```bash
sudo apt install nginx
# Configure nginx as reverse proxy to port 5000
```

**Pros**: Full control, customizable
**Cons**: Requires more DevOps knowledge

---

### Option 6: Azure Container Instances
**Best for**: Quick container deployment on Azure

**Steps:**
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create resource group
az group create --name forecasting-rg --location eastus

# Create container instance
az container create \
  --resource-group forecasting-rg \
  --name forecasting-engine \
  --image your-dockerhub-username/forecasting-engine \
  --dns-name-label forecasting-engine-unique \
  --ports 5000
```

**Pros**: Easy Azure integration
**Cons**: Costs more than serverless options

---

### Option 7: DigitalOcean App Platform
**Best for**: Developer-friendly PaaS

**Steps:**
1. Create account at [digitalocean.com](https://digitalocean.com)
2. Go to "Apps" → "Create App"
3. Connect GitHub repository
4. Select "Web Service"
5. App Platform auto-configures from Dockerfile
6. Deploy

**Pros**: Simple, good pricing, includes database options
**Cons**: Not free tier

---

### Option 8: Docker + Any VPS (Linode, Vultr, etc.)
**Best for**: Budget-conscious, full control

**Steps:**
```bash
# On your VPS (after SSH)
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repo
git clone your-repo-url
cd forecasting-engine

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

**VPS Providers:**
- Linode: $5/month for basic tier
- Vultr: $2.50/month for smallest instance
- Hetzner: €3.79/month for basic VPS

---

## 📋 Pre-Deployment Checklist

### Required Files (all included)
- ✅ `app.py` - Flask application
- ✅ `forecasting_engine.py` - Core forecasting logic
- ✅ `requirements.txt` - Python dependencies
- ✅ `requirements_web.txt` - Web dependencies
- ✅ `Dockerfile` - Container configuration
- ✅ `docker-compose.yml` - Docker Compose config
- ✅ `Procfile` - Heroku configuration
- ✅ `render.yaml` - Render.com configuration
- ✅ `templates/` - HTML templates
- ✅ `static/` - CSS and JS files

### Environment Variables
Most platforms auto-configure, but you may need:
```bash
FLASK_ENV=production
PORT=5000  # Auto-set by most platforms
```

---

## 🔧 Docker Deployment (Universal)

Works on any platform that supports Docker:

### Build Image
```bash
docker build -t forecasting-engine .
```

### Run Locally
```bash
docker run -p 5000:5000 forecasting-engine
```

### Push to Docker Hub (for cloud deployment)
```bash
docker login
docker tag forecasting-engine your-username/forecasting-engine
docker push your-username/forecasting-engine
```

---

## 🌐 Custom Domain Setup

After deployment, point your domain:

### For Render/Heroku/Railway
1. Go to settings → Custom Domains
2. Add your domain (e.g., forecast.yourdomain.com)
3. Update DNS records as instructed

### For AWS/VPS
1. Point A record to your server IP
2. Setup SSL with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d forecast.yourdomain.com
```

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid Start | Best For |
|----------|-----------|------------|----------|
| Render.com | ✅ Yes | $7/mo | Getting started |
| Heroku | ⚠️ Limited | $5/mo | Quick deploy |
| Railway.app | $5 credit | $5/mo | Developers |
| Google Cloud Run | 2M requests/mo | Pay-per-use | Variable traffic |
| AWS EC2 | 750 hrs/mo (1yr) | $10/mo | Production |
| DigitalOcean | ❌ No | $4/mo | Small apps |
| Vultr VPS | ❌ No | $2.50/mo | Budget option |

---

## 🔐 Security Recommendations

### 1. Environment Variables
Never commit sensitive data. Use environment variables:
```python
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-key')
```

### 2. HTTPS
- Most cloud platforms provide free SSL
- For VPS, use Let's Encrypt (free)

### 3. Rate Limiting
Add to `app.py`:
```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
```

### 4. File Upload Limits
Already configured in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
Increase worker count in `Procfile` or `Dockerfile`:
```
--workers 8  # More workers for more concurrent requests
```

### Database (Optional)
For saving results long-term, add PostgreSQL:
```bash
# Heroku
heroku addons:create heroku-postgresql:mini

# Render
# Add PostgreSQL in dashboard
```

### Redis Cache (Optional)
For faster repeated forecasts:
```bash
# Install redis
pip install redis flask-caching
```

---

## 🐛 Troubleshooting

### App won't start
Check logs:
```bash
# Heroku
heroku logs --tail

# Docker
docker-compose logs -f

# Render
View logs in dashboard
```

### Out of memory
Increase instance size or reduce workers:
- Heroku: Upgrade dyno type
- AWS: Use larger EC2 instance
- Docker: Add memory limits to docker-compose.yml

### Slow forecasts
- TFT is very slow - disable for production
- Use caching for repeated forecasts
- Increase timeout in gunicorn config

---

## 🎯 Recommended Deployment Path

### For Beginners:
1. Start with **Render.com** (free, easiest)
2. Test with sample data
3. Share the link

### For Production:
1. Use **AWS EC2** or **Google Cloud Run**
2. Setup custom domain
3. Enable HTTPS
4. Add monitoring (CloudWatch, Datadog)

### For Enterprise:
1. Kubernetes on AWS/GCP/Azure
2. Load balancing
3. Auto-scaling
4. Database for results persistence

---

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review error logs
3. Verify all dependencies installed
4. Check firewall/security group settings

---

## ✅ Quick Test After Deployment

Visit your app URL:
- `/` - Should show web interface
- `/health` - Should return `{"status": "healthy"}`

Upload the sample CSV file and run a forecast to verify everything works!

---

**Ready to deploy? Choose your platform above and follow the steps!** 🚀
