#!/bin/bash
# Build script for Forecasting Engine Docker image

set -e  # Exit on error

echo "========================================="
echo "Forecasting Engine - Docker Build Script"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Are you in the correct directory?"
    exit 1
fi

# Verify required files exist
echo "Checking required files..."
REQUIRED_FILES=(
    "app.py"
    "forecasting_engine.py"
    "requirements.txt"
    "requirements_web.txt"
    "Dockerfile"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file - MISSING!"
        exit 1
    fi
done

# Check directories
echo ""
echo "Checking directories..."
if [ -d "static" ] && [ -d "templates" ]; then
    echo "✓ static/"
    echo "✓ templates/"
else
    echo "Creating missing directories..."
    mkdir -p static/css static/js templates
fi

# Verify files in directories
if [ ! -f "static/css/style.css" ]; then
    echo "Warning: static/css/style.css not found"
fi
if [ ! -f "static/js/app.js" ]; then
    echo "Warning: static/js/app.js not found"
fi
if [ ! -f "templates/index.html" ]; then
    echo "Warning: templates/index.html not found"
fi

# Create upload/results directories
mkdir -p uploads results

echo ""
echo "Building Docker image..."
echo "========================================="
echo ""

# Build with error handling
if docker build -t forecasting-engine .; then
    echo ""
    echo "========================================="
    echo "✓ Build successful!"
    echo "========================================="
    echo ""
    echo "To run the container:"
    echo "  docker run -p 5000:5000 forecasting-engine"
    echo ""
    echo "Or use Docker Compose:"
    echo "  docker-compose up -d"
    echo ""
    echo "Access at: http://localhost:5000"
    echo ""
else
    echo ""
    echo "========================================="
    echo "✗ Build failed!"
    echo "========================================="
    echo ""
    echo "Troubleshooting:"
    echo "1. Check DOCKER_TROUBLESHOOTING.md"
    echo "2. Try: mv Dockerfile.simple Dockerfile"
    echo "3. Or deploy to Render.com (no Docker needed)"
    echo ""
    exit 1
fi
