#!/usr/bin/env python3
"""
Quick test script to verify everything works
"""

import sys
import os

print("=" * 60)
print("FORECASTING ENGINE - SYSTEM CHECK")
print("=" * 60)
print()

# Check Python version
print("✓ Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
else:
    print(f"  ✗ Python {sys.version_info.major}.{sys.version_info.minor} - UPGRADE NEEDED (3.8+ required)")
    sys.exit(1)

print()

# Check required files
print("✓ Checking required files...")
required_files = [
    'forecasting_engine.py',
    'app_standalone.py',
    'requirements.txt',
    'requirements_web.txt',
    'sample_data.csv'
]

all_files_present = True
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING!")
        all_files_present = False

if not all_files_present:
    print("\n✗ Some required files are missing!")
    sys.exit(1)

print()

# Try importing required packages
print("✓ Checking Python packages...")

packages = [
    ('pandas', 'pandas'),
    ('numpy', 'numpy'),
    ('sklearn', 'scikit-learn'),
    ('flask', 'Flask'),
]

missing_packages = []

for import_name, package_name in packages:
    try:
        __import__(import_name)
        print(f"  ✓ {package_name}")
    except ImportError:
        print(f"  ✗ {package_name} - NOT INSTALLED")
        missing_packages.append(package_name)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print("   Install with: pip install -r requirements.txt -r requirements_web.txt")
else:
    print("\n✓ All core packages installed!")

print()

# Check optional packages
print("✓ Checking forecasting packages (optional)...")

forecasting_packages = [
    ('statsmodels', 'statsmodels'),
    ('prophet', 'prophet'),
    ('xgboost', 'xgboost'),
]

for import_name, package_name in forecasting_packages:
    try:
        __import__(import_name)
        print(f"  ✓ {package_name}")
    except ImportError:
        print(f"  ⚠️  {package_name} - NOT INSTALLED (some methods will be disabled)")

print()

# Test basic functionality
print("✓ Testing forecasting engine...")
try:
    from forecasting_engine import ForecastingEngine, create_sample_data
    df = create_sample_data()
    print(f"  ✓ Created sample data: {len(df)} rows")
    
    engine = ForecastingEngine(df=df)
    print(f"  ✓ Initialized engine")
    
    engine.split_data(test_size=0.2)
    print(f"  ✓ Split data: {len(engine.train)} train, {len(engine.test)} test")
    
    print("\n✅ ENGINE TEST PASSED!")
except Exception as e:
    print(f"\n✗ ENGINE TEST FAILED: {str(e)}")
    sys.exit(1)

print()
print("=" * 60)
print("SYSTEM CHECK COMPLETE")
print("=" * 60)
print()
print("✅ Your system is ready!")
print()
print("Next steps:")
print("1. Run locally: python app_standalone.py")
print("2. Or deploy to Render.com (see NO_DOCKER_DEPLOY.md)")
print("3. Or test with Python: python -i forecasting_engine.py")
print()
print("For help, see: START_HERE.md")
print("=" * 60)
