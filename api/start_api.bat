@echo off
echo ========================================
echo    MANVUE API LAUNCHER (Windows)
echo ========================================
echo.
echo Starting ManVue API services...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Start the API launcher
python launch_api.py

pause
