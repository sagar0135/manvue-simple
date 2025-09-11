@echo off
echo ================================
echo MANVUE Image Setup for Windows
echo ================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)
echo ✓ Python is available

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [3/4] Starting MongoDB image setup...
echo This will download images and store them in your MongoDB database...
python setup_manvue_images.py
if errorlevel 1 (
    echo ERROR: Setup failed - check the output above
    pause
    exit /b 1
)

echo.
echo [4/4] Setup completed!
echo ✓ Images converted to GridFS
echo ✓ Products seeded in database
echo ✓ API ready to serve images
echo.
echo Next steps:
echo 1. Start your API server: python ../start_enhanced_backend.py
echo 2. Test the API: http://localhost:5001/api/products
echo 3. Update your frontend with the new product IDs
echo.
pause
