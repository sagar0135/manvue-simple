#!/usr/bin/env python3
"""
ManVue API Launcher
Easy access to all API services and commands
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
    print("🚀 MANVUE API LAUNCHER")
    print("=" * 60)
    print("📋 Available API Services:")
    print("   1. Enhanced API (with ML features)")
    print("   2. Simple API (basic functionality)")
    print("   3. ML API Server (fashion recognition)")
    print("   4. All Services (complete platform)")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import requests
        print("✅ Backend dependencies: OK")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Run: pip install -r ../backend/requirements.txt")
        return False

def start_enhanced_api():
    """Start the enhanced API with ML features"""
    print("🤖 Starting Enhanced API with ML features...")
    print("📍 API: http://localhost:5000")
    print("📍 Docs: http://localhost:5000/docs")
    
    try:
        subprocess.run([sys.executable, "enhanced_main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Enhanced API failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Enhanced API stopped")

def start_simple_api():
    """Start the simple API"""
    print("⚡ Starting Simple API...")
    print("📍 API: http://localhost:5000")
    print("📍 Docs: http://localhost:5000/docs")
    
    try:
        subprocess.run([sys.executable, "simple_main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Simple API failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Simple API stopped")

def start_ml_api():
    """Start the ML API server"""
    print("🧠 Starting ML API Server...")
    print("📍 ML API: http://localhost:5001")
    
    ml_server_path = Path("../backend/ML/start_ml_server.py")
    if ml_server_path.exists():
        try:
            subprocess.run([sys.executable, str(ml_server_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ ML API failed: {e}")
        except KeyboardInterrupt:
            print("🛑 ML API stopped")
    else:
        print("❌ ML server not found. Please check backend/ML/ directory")

def start_all_services():
    """Start all services (enhanced API + ML)"""
    print("🚀 Starting All Services...")
    
    # Start ML API in background
    ml_thread = threading.Thread(target=start_ml_api, daemon=True)
    ml_thread.start()
    
    # Wait a bit for ML to start
    time.sleep(3)
    
    # Start enhanced API (this will block)
    start_enhanced_api()

def open_api_docs():
    """Open API documentation in browser"""
    time.sleep(2)
    print("🌐 Opening API documentation...")
    webbrowser.open("http://localhost:5000/docs")

def show_api_commands():
    """Show useful API commands"""
    print("\n📋 Useful API Commands:")
    print("=" * 40)
    print("🔍 Test API Health:")
    print("   curl http://localhost:5000/")
    print()
    print("📦 Get Products:")
    print("   curl http://localhost:5000/products")
    print()
    print("🔍 AI Text Search:")
    print('   curl -X POST http://localhost:5000/products/search \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"query": "cotton shirt", "category": "tops"}\'')
    print()
    print("📸 AI Image Search:")
    print('   curl -X POST http://localhost:5000/products/image-search \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"image": "data:image/jpeg;base64,..."}\'')
    print()
    print("➕ Add Product:")
    print('   curl -X POST http://localhost:5000/products \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"title": "New Shirt", "price": 29.99, "category": "tops"}\'')
    print()
    print("🛠️ Admin Products:")
    print("   curl http://localhost:5000/admin/products")
    print("=" * 40)

def main():
    print_banner()
    
    if not check_dependencies():
        return
    
    while True:
        print("\n🎯 Select API Service:")
        print("1. Enhanced API (with ML features)")
        print("2. Simple API (basic functionality)")
        print("3. ML API Server only")
        print("4. All Services (enhanced + ML)")
        print("5. Show API Commands")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting Enhanced API...")
            browser_thread = threading.Thread(target=open_api_docs, daemon=True)
            browser_thread.start()
            start_enhanced_api()
            break
            
        elif choice == "2":
            print("\n⚡ Starting Simple API...")
            browser_thread = threading.Thread(target=open_api_docs, daemon=True)
            browser_thread.start()
            start_simple_api()
            break
            
        elif choice == "3":
            print("\n🧠 Starting ML API Server...")
            start_ml_api()
            break
            
        elif choice == "4":
            print("\n🚀 Starting All Services...")
            browser_thread = threading.Thread(target=open_api_docs, daemon=True)
            browser_thread.start()
            start_all_services()
            break
            
        elif choice == "5":
            show_api_commands()
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
