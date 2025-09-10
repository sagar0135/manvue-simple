#!/usr/bin/env python3
"""
ManVue Complete Startup Script
Starts both frontend and backend servers with enhanced features
"""
import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🚀 MANVUE - AI-Powered Fashion E-commerce Platform")
    print("=" * 60)
    print("✨ Features:")
    print("   - AI-powered text and image search")
    print("   - Product management system")
    print("   - ML integration for fashion recognition")
    print("   - Responsive design with modern UI")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import requests
        print("✅ Backend dependencies: OK")
    except ImportError as e:
        print(f"❌ Missing backend dependencies: {e}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    
    return True

def start_backend():
    """Start the enhanced backend server"""
    print("🔧 Starting Enhanced Backend Server...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    try:
        # Start the enhanced backend
        subprocess.run([
            sys.executable, "enhanced_main.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("🛑 Backend stopped by user")
        return False

def start_frontend():
    """Start the frontend server"""
    print("🎨 Starting Frontend Server...")
    
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        # Start HTTP server
        subprocess.run([
            sys.executable, "-m", "http.server", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("🛑 Frontend stopped by user")
        return False

def wait_for_backend():
    """Wait for backend to be ready"""
    import requests
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:5000/", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"⏳ Waiting for backend... ({attempt + 1}/{max_attempts})")
    
    print("❌ Backend failed to start within timeout")
    return False

def open_browser():
    """Open browser to the application"""
    time.sleep(2)  # Give servers time to start
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:8000")

def main():
    print_banner()
    
    if not check_dependencies():
        return
    
    print("\n🚀 Starting ManVue Platform...")
    print("📍 Frontend: http://localhost:8000")
    print("📍 Backend API: http://localhost:5000")
    print("📍 API Docs: http://localhost:5000/docs")
    print("\n🛑 Press Ctrl+C to stop all servers")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to be ready
    if not wait_for_backend():
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start frontend (this will block)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down ManVue...")
        print("✅ All servers stopped. Goodbye!")

if __name__ == "__main__":
    main()
