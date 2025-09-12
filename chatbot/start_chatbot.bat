@echo off
REM ManVue Chatbot Startup Script for Windows

echo ==============================================
echo 🤖 ManVue Fashion Chatbot Startup
echo ==============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8 or higher.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "config.yml" (
    echo ❌ config.yml not found! 
    echo 💡 Make sure you're running this from the chatbot directory.
    pause
    exit /b 1
)

echo ✅ Python found
echo 📁 Current directory: %CD%

REM Install/upgrade dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

REM Start the chatbot system
echo.
echo 🚀 Starting ManVue Chatbot System...
python start_chatbot.py

echo.
echo 👋 Chatbot system stopped.
pause

