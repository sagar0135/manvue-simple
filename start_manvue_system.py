#!/usr/bin/env python3
"""
ManVue Complete System Startup Script
Starts all services: Product Generator, Auth API, Chatbot Server, and Frontend
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

class ManVueSystemStarter:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent
        
    def start_product_generator(self):
        """Generate product HTML files"""
        print("🏭 Generating product HTML files...")
        try:
            result = subprocess.run([
                sys.executable, 
                str(self.base_dir / "product_generator.py")
            ], capture_output=True, text=True, cwd=self.base_dir)
            
            if result.returncode == 0:
                print("✅ Product HTML files generated successfully")
            else:
                print(f"❌ Product generation failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Error generating products: {e}")
    
    def start_auth_api(self):
        """Start the authentication and payment API"""
        print("🔐 Starting Auth & Payment API...")
        try:
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn",
                "api.auth_payment_api:app",
                "--host", "0.0.0.0",
                "--port", "8001",
                "--reload"
            ], cwd=self.base_dir)
            self.processes.append(("Auth API", process))
            print("✅ Auth & Payment API started on http://localhost:8001")
        except Exception as e:
            print(f"❌ Failed to start Auth API: {e}")
    
    def start_chatbot_server(self):
        """Start the chatbot server"""
        print("🤖 Starting Chatbot Server...")
        try:
            process = subprocess.Popen([
                sys.executable,
                str(self.base_dir / "chatbot" / "chatbot_server.py")
            ], cwd=self.base_dir)
            self.processes.append(("Chatbot Server", process))
            print("✅ Chatbot Server started on http://localhost:5055")
        except Exception as e:
            print(f"❌ Failed to start Chatbot Server: {e}")
    
    def start_frontend_server(self):
        """Start the frontend development server"""
        print("🌐 Starting Frontend Server...")
        try:
            # Try to use Python's built-in HTTP server
            process = subprocess.Popen([
                sys.executable, "-m", "http.server", "3000"
            ], cwd=str(self.base_dir / "frontend"))
            self.processes.append(("Frontend Server", process))
            print("✅ Frontend Server started on http://localhost:3000")
        except Exception as e:
            print(f"❌ Failed to start Frontend Server: {e}")
    
    def open_browser(self):
        """Open browser after a delay"""
        def delayed_open():
            time.sleep(3)
            try:
                webbrowser.open("http://localhost:3000")
                print("🌐 Opening browser...")
            except Exception as e:
                print(f"❌ Failed to open browser: {e}")
        
        thread = threading.Thread(target=delayed_open)
        thread.daemon = True
        thread.start()
    
    def monitor_processes(self):
        """Monitor running processes"""
        while True:
            time.sleep(5)
            for name, process in self.processes:
                if process.poll() is not None:
                    print(f"⚠️  {name} has stopped unexpectedly")
                    self.processes.remove((name, process))
    
    def cleanup(self):
        """Clean up all processes"""
        print("\n🛑 Shutting down all services...")
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️  {name} force stopped")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "pymongo", "stripe", 
            "python-dotenv", "pydantic", "requests"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("📦 Installing missing packages...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r",
                    str(self.base_dir / "api" / "requirements.txt")
                ], check=True)
                print("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                return False
        
        return True
    
    def create_env_file(self):
        """Create .env file if it doesn't exist"""
        env_file = self.base_dir / ".env"
        if not env_file.exists():
            print("📝 Creating .env file...")
            env_content = """# ManVue Environment Configuration

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Stripe Configuration (Get these from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
CHATBOT_PORT=5055
FRONTEND_PORT=3000
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ .env file created. Please update with your actual API keys.")
    
    def run(self):
        """Main run method"""
        print("🚀 Starting ManVue Complete System...")
        print("=" * 50)
        
        try:
            # Check dependencies
            if not self.check_dependencies():
                print("❌ Dependency check failed. Please install required packages.")
                return
            
            # Create .env file
            self.create_env_file()
            
            # Generate product HTML files
            self.start_product_generator()
            
            # Start all services
            self.start_auth_api()
            time.sleep(2)
            
            self.start_chatbot_server()
            time.sleep(2)
            
            self.start_frontend_server()
            time.sleep(2)
            
            # Open browser
            self.open_browser()
            
            print("\n" + "=" * 50)
            print("🎉 ManVue System Started Successfully!")
            print("=" * 50)
            print("📱 Frontend: http://localhost:3000")
            print("🔐 Auth API: http://localhost:8001")
            print("🤖 Chatbot: http://localhost:5055")
            print("📚 API Docs: http://localhost:8001/docs")
            print("=" * 50)
            print("Press Ctrl+C to stop all services")
            
            # Monitor processes
            self.monitor_processes()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested by user")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    starter = ManVueSystemStarter()
    starter.run()
