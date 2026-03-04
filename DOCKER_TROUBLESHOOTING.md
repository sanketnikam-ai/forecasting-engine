# Docker Deployment Troubleshooting

## Error: "static": not found

This error occurs when Docker can't find the static directory during build.

### Solutions:

#### Solution 1: Use the Simple Dockerfile
```bash
# Rename the simple Dockerfile
mv Dockerfile Dockerfile.backup
mv Dockerfile.simple Dockerfile

# Build
docker build -t forecasting-engine .
```

#### Solution 2: Ensure Directory Structure
Make sure you have this structure:
```
your-project/
├── app.py
├── forecasting_engine.py
├── requirements.txt
├── requirements_web.txt
├── Dockerfile
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── templates/
    └── index.html
```

Verify with:
```bash
ls -la static/
ls -la templates/
```

#### Solution 3: Build from the Correct Directory
```bash
# Make sure you're in the directory with Dockerfile
cd /path/to/your/project

# Check files are present
ls -la

# Then build
docker build -t forecasting-engine .
```

#### Solution 4: Use Docker Ignore
The `.dockerignore` file is included. Make sure it's in the same directory as Dockerfile.

#### Solution 5: Manual File Creation
If directories are missing, create them:

```bash
# Create directories
mkdir -p static/css static/js templates uploads results

# Copy the CSS file (create if missing)
cat > static/css/style.css << 'EOF'
/* Minimal CSS - replace with full version from static/css/style.css */
body { font-family: Arial, sans-serif; margin: 20px; }
.container { max-width: 1200px; margin: 0 auto; }
EOF

# Copy the JS file (create if missing)
cat > static/js/app.js << 'EOF'
// Minimal JS - replace with full version from static/js/app.js
console.log('Forecasting Engine loaded');
EOF

# Copy the HTML template (create if missing)
cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Forecasting Engine</title></head>
<body><h1>Forecasting Engine</h1></body>
</html>
EOF
```

---

## Alternative: Deploy Without Docker

If Docker continues to have issues, deploy directly:

### Method 1: Direct Python Deployment

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements_web.txt

# Run directly
python app.py
```

### Method 2: Use Gunicorn Directly

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements_web.txt

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 300 app:app
```

### Method 3: Deploy to Render.com (No Docker Needed!)

Render.com doesn't require Docker. Just:

1. Push your code to GitHub
2. Connect to Render.com
3. Render builds automatically from `render.yaml`

**This is the easiest option!**

---

## Testing Your Build

### Test 1: Check Files Exist
```bash
# List all files
find . -type f | grep -E "(static|templates)"

# Should show:
# ./static/css/style.css
# ./static/js/app.js
# ./templates/index.html
```

### Test 2: Build with Verbose Output
```bash
docker build --progress=plain -t forecasting-engine . 2>&1 | tee build.log
```

### Test 3: Build Without Cache
```bash
docker build --no-cache -t forecasting-engine .
```

### Test 4: Check Docker Context
```bash
docker build --progress=plain -t forecasting-engine . 2>&1 | grep "COPY"
```

---

## Common Issues and Fixes

### Issue: "No such file or directory"
**Fix**: Verify you're in the correct directory
```bash
pwd  # Should show your project directory
ls   # Should show Dockerfile, app.py, etc.
```

### Issue: Permission Denied
**Fix**: Run with sudo or fix permissions
```bash
sudo docker build -t forecasting-engine .
# OR
sudo chmod -R 755 static templates
```

### Issue: Build is Slow
**Fix**: Use .dockerignore (included) to skip unnecessary files

### Issue: Dependencies Won't Install
**Fix**: Check internet connection or use a base image with dependencies
```dockerfile
FROM python:3.10-slim
# Add: --no-cache-dir to pip install commands
```

---

## Recommended: Skip Docker for Now

The **easiest path** if Docker is giving issues:

### Option A: Render.com (Recommended)
1. Upload your code to GitHub
2. Go to render.com
3. Create Web Service
4. Point to your repo
5. Deploy!

Render builds the container for you - no Docker expertise needed!

### Option B: Heroku
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create and deploy
heroku create my-forecasting-app
git push heroku main
```

### Option C: Run Locally
```bash
pip install -r requirements.txt -r requirements_web.txt
python app.py
# Visit http://localhost:5000
```

---

## Still Having Issues?

### Quick Fix: Use the All-in-One Build Script

```bash
#!/bin/bash
# save as build.sh

# Create directories
mkdir -p static/css static/js templates uploads results

# Ensure files exist (copy your actual content)
if [ ! -f "static/css/style.css" ]; then
    echo "body { margin: 20px; }" > static/css/style.css
fi

if [ ! -f "static/js/app.js" ]; then
    echo "console.log('loaded');" > static/js/app.js
fi

if [ ! -f "templates/index.html" ]; then
    echo "<h1>Forecasting Engine</h1>" > templates/index.html
fi

# Build
docker build -t forecasting-engine .

echo "Build complete! Run with: docker run -p 5000:5000 forecasting-engine"
```

Run it:
```bash
chmod +x build.sh
./build.sh
```

---

## Contact Support

If none of these work:
1. Share the complete error message
2. Share output of: `ls -la`
3. Share output of: `cat Dockerfile`
4. Try Render.com instead (bypasses Docker issues entirely)

**Recommended: Use Render.com - it's free and handles all the Docker complexity for you!**
