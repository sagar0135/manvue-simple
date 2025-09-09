#!/usr/bin/env python3
"""
MANVUE ML Server Startup Script
Starts the ML API server and checks all dependencies
"""

import os
import sys
import subprocess
import platform
import time
import requests
import json

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pydantic', 'tensorflow', 'numpy', 'pillow', 'opencv-python'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_model_files():
    """Check if model files exist"""
    model_path = 'models/fashion_classifier.h5'
    metadata_path = 'models/model_metadata.json'
    
    if os.path.exists(model_path):
        print(f"✅ Model file found: {model_path}")
        model_exists = True
    else:
        print(f"⚠️  Model file not found: {model_path}")
        print("   Using demo model fallback")
        model_exists = False
    
    if os.path.exists(metadata_path):
        print(f"✅ Metadata file found: {metadata_path}")
    else:
        print(f"ℹ️  Metadata file not found: {metadata_path}")
        print("   Will create default metadata")
    
    return model_exists

def create_directories():
    """Create necessary directories"""
    directories = [
        'models', 'data/raw', 'data/processed', 'data/augmented',
        'notebooks/checkpoints', 'api/logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def start_server():
    """Start the ML API server"""
    print("\n🚀 Starting MANVUE ML API Server...")
    
    try:
        # Change to API directory
        os.chdir('api')
        
        # Start the server
        if platform.system() == "Windows":
            # Windows
            subprocess.Popen([sys.executable, 'ml_server.py'])
        else:
            # Unix-like systems
            subprocess.Popen([sys.executable, 'ml_server.py'])
        
        print("⏳ Server starting...")
        time.sleep(3)
        
        # Test server
        try:
            response = requests.get('http://localhost:5000/health', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ ML API Server is running!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Model Loaded: {data.get('model_loaded', False)}")
                print(f"   Version: {data.get('version', 'unknown')}")
                return True
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Failed to connect to server: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def show_usage_info():
    """Display usage information"""
    print("\n" + "="*60)
    print("🎯 MANVUE ML API Server (FastAPI)")
    print("="*60)
    print("📊 API Endpoints:")
    print("   • GET  /health     - Server health check")
    print("   • POST /predict    - Image classification")
    print("   • GET  /categories - Available categories")
    print("   • POST /retrain    - Model retraining")
    print()
    print("📚 Auto-Generated Documentation:")
    print("   • Swagger UI: http://localhost:5000/docs")
    print("   • ReDoc: http://localhost:5000/redoc")
    print()
    print("🔗 Integration:")
    print("   • Server: http://localhost:5000")
    print("   • Frontend: Enhanced ML integration")
    print("   • Notebooks: Jupyter available for training")
    print()
    print("📁 Project Structure:")
    print("   • models/     - Trained ML models")
    print("   • data/       - Training datasets")
    print("   • notebooks/  - Jupyter notebooks")
    print("   • api/        - FastAPI server")
    print("   • utils/      - Integration utilities")
    print()
    print("🚀 FastAPI Features:")
    print("   • Async/await support for better performance")
    print("   • Automatic request/response validation")
    print("   • Interactive API documentation")
    print("   • Background tasks for long operations")
    print()
    print("🛠️  Commands:")
    print("   • python start_ml_server.py  - Start FastAPI server")
    print("   • pip install -r requirements.txt  - Install deps")
    print("   • jupyter notebook  - Open training notebooks")
    print("="*60)

def main():
    """Main startup routine"""
    print("🤖 MANVUE ML Server Setup")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        install_choice = input("Install missing packages? (y/n): ").lower().strip()
        
        if install_choice == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("❌ Cannot start without required packages")
            sys.exit(1)
    
    # Check model files
    check_model_files()
    
    # Start server
    if start_server():
        show_usage_info()
        print("\n💡 Tip: Keep this terminal open to see server logs")
        print("🔄 To stop the server, press Ctrl+C")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down ML server...")
            print("✅ Server stopped")
    else:
        print("\n❌ Failed to start ML server")
        print("💡 Check the logs above for error details")
        sys.exit(1)

if __name__ == "__main__":
    main()
