#!/usr/bin/env python3
"""
ManVue Chatbot Startup Script
Handles all chatbot services startup and management
"""

import subprocess
import sys
import time
import requests
import os
import threading
from pathlib import Path

class ChatbotManager:
    def __init__(self):
        self.chatbot_dir = Path(__file__).parent
        self.processes = []
        self.rasa_port = 5005
        self.action_port = 5055
        self.integration_port = 5055
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        try:
            import rasa
            print(f"✅ Rasa: {rasa.__version__}")
        except ImportError:
            print("❌ Rasa not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            
        try:
            import fastapi
            print(f"✅ FastAPI: {fastapi.__version__}")
        except ImportError:
            print("❌ FastAPI not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
            
        print("✅ Dependencies check complete!")
        
    def train_model(self):
        """Train the Rasa model if needed"""
        model_path = self.chatbot_dir / "models"
        
        if not model_path.exists() or not list(model_path.glob("*.tar.gz")):
            print("🤖 Training Rasa model...")
            try:
                result = subprocess.run([
                    "rasa", "train",
                    "--config", "config.yml",
                    "--domain", "domain.yml",
                    "--data", "data"
                ], cwd=self.chatbot_dir, check=True, capture_output=True, text=True)
                
                print("✅ Model training completed!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Model training failed: {e}")
                print(f"Output: {e.stdout}")
                print(f"Error: {e.stderr}")
                return False
        else:
            print("✅ Model already exists, skipping training")
            return True
    
    def start_rasa_server(self):
        """Start the Rasa server"""
        print(f"🚀 Starting Rasa server on port {self.rasa_port}...")
        
        try:
            process = subprocess.Popen([
                "rasa", "run",
                "--enable-api",
                "--cors", "*",
                "--port", str(self.rasa_port)
            ], cwd=self.chatbot_dir)
            
            self.processes.append(('Rasa Server', process))
            
            # Wait for server to start
            self.wait_for_service(f"http://localhost:{self.rasa_port}/status", "Rasa server")
            print(f"✅ Rasa server running on http://localhost:{self.rasa_port}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Rasa server: {e}")
            return False
    
    def start_action_server(self):
        """Start the Rasa action server"""
        print(f"🎬 Starting Rasa action server on port {self.action_port}...")
        
        try:
            process = subprocess.Popen([
                "rasa", "run", "actions",
                "--port", str(self.action_port)
            ], cwd=self.chatbot_dir)
            
            self.processes.append(('Action Server', process))
            
            # Wait for server to start
            time.sleep(3)  # Actions server doesn't have a status endpoint
            print(f"✅ Action server running on http://localhost:{self.action_port}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start action server: {e}")
            return False
    
    def start_integration_server(self):
        """Start the ManVue integration server"""
        print(f"🔗 Starting ManVue integration server on port {self.integration_port}...")
        
        try:
            server_file = self.chatbot_dir / "chatbot_server.py"
            process = subprocess.Popen([
                sys.executable, str(server_file)
            ], cwd=self.chatbot_dir)
            
            self.processes.append(('Integration Server', process))
            
            # Wait for server to start
            self.wait_for_service(f"http://localhost:{self.integration_port}/health", "Integration server")
            print(f"✅ Integration server running on http://localhost:{self.integration_port}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start integration server: {e}")
            return False
    
    def wait_for_service(self, url, service_name, max_attempts=30):
        """Wait for a service to become available"""
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=2)
                if response.status_code in [200, 404]:  # 404 is OK for some endpoints
                    return True
            except:
                pass
            
            print(f"⏳ Waiting for {service_name}... ({attempt + 1}/{max_attempts})")
            time.sleep(2)
        
        print(f"⚠️ {service_name} may not be fully ready")
        return False
    
    def check_manvue_api(self):
        """Check if ManVue API is running"""
        try:
            response = requests.get("http://localhost:5000/", timeout=3)
            if response.status_code == 200:
                print("✅ ManVue API is running")
                return True
        except:
            pass
        
        print("⚠️ ManVue API not detected on port 5000")
        print("💡 Make sure to start the ManVue backend first!")
        return False
    
    def open_browser(self):
        """Open browser to chatbot interface"""
        try:
            import webbrowser
            url = f"http://localhost:{self.integration_port}"
            print(f"🌐 Opening browser to {url}")
            webbrowser.open(url)
        except Exception as e:
            print(f"💻 Please open http://localhost:{self.integration_port} in your browser")
    
    def show_status(self):
        """Show status of all services"""
        print("\n" + "="*50)
        print("📊 ManVue Chatbot Status")
        print("="*50)
        print(f"🤖 Rasa Server: http://localhost:{self.rasa_port}")
        print(f"🎬 Action Server: http://localhost:{self.action_port}")
        print(f"🔗 Integration Server: http://localhost:{self.integration_port}")
        print(f"🌐 Chatbot Interface: http://localhost:{self.integration_port}")
        print("\n📱 To integrate with ManVue frontend:")
        print("   Include the chatbot widget in your HTML files")
        print("   WebSocket endpoint: ws://localhost:5055/ws")
        print("\n⚠️ Press Ctrl+C to stop all services")
        print("="*50)
    
    def cleanup(self):
        """Clean up all processes"""
        print("\n🛑 Stopping all chatbot services...")
        
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {name}")
            except:
                try:
                    process.kill()
                    print(f"🔪 Force killed {name}")
                except:
                    print(f"❌ Failed to stop {name}")
        
        print("👋 All services stopped!")
    
    def start_all(self):
        """Start all chatbot services"""
        print("🚀 Starting ManVue Chatbot System")
        print("="*40)
        
        # Check dependencies
        self.check_dependencies()
        
        # Check ManVue API
        self.check_manvue_api()
        
        # Train model if needed
        if not self.train_model():
            print("❌ Model training failed. Chatbot may not work properly.")
        
        # Start services
        services_started = 0
        
        if self.start_rasa_server():
            services_started += 1
        
        if self.start_action_server():
            services_started += 1
        
        if self.start_integration_server():
            services_started += 1
        
        if services_started == 3:
            print("\n🎉 All services started successfully!")
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
    manager = ChatbotManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "train":
            manager.train_model()
        elif command == "status":
            manager.show_status()
        elif command == "stop":
            manager.cleanup()
        else:
            print("Usage: python start_chatbot.py [train|status|stop]")
    else:
        manager.start_all()

if __name__ == "__main__":
    main()

