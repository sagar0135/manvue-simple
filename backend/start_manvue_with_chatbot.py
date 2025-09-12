#!/usr/bin/env python3
"""
Enhanced ManVue Startup Script with Chatbot Integration
Starts both ManVue platform and the integrated chatbot system
"""

import subprocess
import sys
import time
import webbrowser
import threading
import requests
from pathlib import Path

class ManVueWithChatbot:
    def __init__(self):
        self.processes = []
        self.services = {
            'ManVue Backend': {'port': 5000, 'process': None, 'url': 'http://localhost:5000'},
            'ManVue Frontend': {'port': 8000, 'process': None, 'url': 'http://localhost:8000'},
            'Rasa Server': {'port': 5005, 'process': None, 'url': 'http://localhost:5005'},
            'Chatbot Integration': {'port': 5055, 'process': None, 'url': 'http://localhost:5055'}
        }
    
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        print("🔍 Checking dependencies...")
        
        # Check Python packages
        required_packages = ['fastapi', 'uvicorn', 'rasa']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} installed")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} not found")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        
        print("✅ Dependencies check complete!")
        return True
    
    def start_manvue_backend(self):
        """Start ManVue backend API"""
        print("🚀 Starting ManVue Backend...")
        
        try:
            # Try enhanced backend first
            api_file = Path("api/enhanced_main.py")
            if api_file.exists():
                process = subprocess.Popen([
                    sys.executable, str(api_file)
                ], cwd="api")
            else:
                # Fallback to simple backend
                backend_file = Path("backend/main.py")
                if backend_file.exists():
                    process = subprocess.Popen([
                        sys.executable, str(backend_file)
                    ], cwd="backend")
                else:
                    print("❌ No backend found!")
                    return False
            
            self.services['ManVue Backend']['process'] = process
            self.wait_for_service('http://localhost:5000', 'ManVue Backend')
            print("✅ ManVue Backend running on http://localhost:5000")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start ManVue Backend: {e}")
            return False
    
    def start_manvue_frontend(self):
        """Start ManVue frontend server"""
        print("🌐 Starting ManVue Frontend...")
        
        try:
            process = subprocess.Popen([
                sys.executable, "-m", "http.server", "8000"
            ], cwd="frontend")
            
            self.services['ManVue Frontend']['process'] = process
            time.sleep(2)  # HTTP server starts quickly
            print("✅ ManVue Frontend running on http://localhost:8000")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start ManVue Frontend: {e}")
            return False
    
    def start_chatbot_system(self):
        """Start the complete chatbot system"""
        print("🤖 Starting Chatbot System...")
        
        try:
            # Train Rasa model if needed
            self.train_chatbot_model()
            
            # Start Rasa server
            rasa_process = subprocess.Popen([
                "rasa", "run",
                "--enable-api",
                "--cors", "*",
                "--port", "5005"
            ], cwd="chatbot")
            
            self.services['Rasa Server']['process'] = rasa_process
            
            # Start chatbot integration server
            integration_process = subprocess.Popen([
                sys.executable, "chatbot_server.py"
            ], cwd="chatbot")
            
            self.services['Chatbot Integration']['process'] = integration_process
            
            # Wait for services
            self.wait_for_service('http://localhost:5005/status', 'Rasa Server')
            self.wait_for_service('http://localhost:5055/health', 'Chatbot Integration')
            
            print("✅ Chatbot System running")
            print("   🤖 Rasa Server: http://localhost:5005")
            print("   🔗 Integration: http://localhost:5055")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Chatbot System: {e}")
            return False
    
    def train_chatbot_model(self):
        """Train the chatbot model if needed"""
        model_path = Path("chatbot/models")
        
        if not model_path.exists() or not list(model_path.glob("*.tar.gz")):
            print("🧠 Training chatbot model...")
            try:
                subprocess.run([
                    "rasa", "train"
                ], cwd="chatbot", check=True, capture_output=True)
                print("✅ Model training completed!")
            except subprocess.CalledProcessError as e:
                print("⚠️ Model training failed, using fallback responses")
    
    def wait_for_service(self, url, service_name, max_attempts=15):
        """Wait for a service to become available"""
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=2)
                if response.status_code in [200, 404]:
                    return True
            except:
                pass
            
            print(f"⏳ Waiting for {service_name}... ({attempt + 1}/{max_attempts})")
            time.sleep(2)
        
        print(f"⚠️ {service_name} may not be fully ready")
        return False
    
    def open_browser(self):
        """Open browser to ManVue with chatbot"""
        try:
            print("🌐 Opening ManVue in browser...")
            webbrowser.open('http://localhost:8000')
            time.sleep(2)
            print("💬 Chatbot widget should appear in the bottom-right corner!")
        except Exception as e:
            print(f"💻 Please open http://localhost:8000 in your browser")
    
    def show_status(self):
        """Show status of all services"""
        print("\n" + "="*60)
        print("🎉 ManVue + Chatbot Platform Ready!")
        print("="*60)
        
        for service_name, info in self.services.items():
            status = "🟢 Running" if info['process'] and info['process'].poll() is None else "🔴 Stopped"
            print(f"{service_name:20} {status:12} {info['url']}")
        
        print("\n📱 Features Available:")
        print("   • 🛍️ E-commerce Platform: Product browsing, search, cart")
        print("   • 🤖 AI Chatbot: Fashion advice, size guide, customer support")
        print("   • 🎤 Voice Search: Speech-to-text product search")
        print("   • 📱 Responsive Design: Works on all devices")
        print("   • 🔍 Visual Search: AI-powered image search")
        
        print("\n💬 Chatbot Commands to Try:")
        print("   • 'Show me popular products'")
        print("   • 'I need help with sizing'")
        print("   • 'What's on sale?'")
        print("   • 'Help me find a jacket'")
        print("   • 'How do I return an item?'")
        
        print("\n⚠️ Press Ctrl+C to stop all services")
        print("="*60)
    
    def cleanup(self):
        """Stop all services"""
        print("\n🛑 Stopping all services...")
        
        for service_name, info in self.services.items():
            if info['process']:
                try:
                    info['process'].terminate()
                    info['process'].wait(timeout=5)
                    print(f"✅ Stopped {service_name}")
                except:
                    try:
                        info['process'].kill()
                        print(f"🔪 Force stopped {service_name}")
                    except:
                        print(f"❌ Failed to stop {service_name}")
        
        print("👋 All services stopped! Thanks for using ManVue!")
    
    def start_all(self):
        """Start all services"""
        print("🚀 Starting ManVue Platform with Chatbot")
        print("="*50)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Start services
        services_started = 0
        
        if self.start_manvue_backend():
            services_started += 1
        
        if self.start_manvue_frontend():
            services_started += 1
        
        if self.start_chatbot_system():
            services_started += 1
        
        if services_started >= 2:  # At least frontend + backend
            print(f"\n🎉 {services_started}/3 services started successfully!")
            self.show_status()
            self.open_browser()
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            print(f"\n⚠️ Only {services_started}/3 services started successfully")
        
        self.cleanup()

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            # Run chatbot tests
            subprocess.run([sys.executable, "chatbot/test_chatbot.py"])
        elif command == "chatbot-only":
            # Start only chatbot
            subprocess.run([sys.executable, "chatbot/start_chatbot.py"])
        elif command == "backend-only":
            # Start only ManVue backend
            subprocess.run([sys.executable, "api/enhanced_main.py"])
        else:
            print("Usage: python start_manvue_with_chatbot.py [test|chatbot-only|backend-only]")
    else:
        platform = ManVueWithChatbot()
        platform.start_all()

if __name__ == "__main__":
    main()

