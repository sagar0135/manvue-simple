#!/usr/bin/env python3
"""
ManVue Chatbot Integration Test
Tests all chatbot components and integrations
"""

import requests
import time
import json
import sys
from pathlib import Path

class ChatbotTester:
    def __init__(self):
        self.rasa_url = "http://localhost:5005"
        self.action_url = "http://localhost:5055"
        self.integration_url = "http://localhost:5055"
        self.manvue_api_url = "http://localhost:5000"
        self.test_results = []
        
    def run_all_tests(self):
        """Run all chatbot tests"""
        print("🧪 Starting ManVue Chatbot Integration Tests")
        print("=" * 50)
        
        tests = [
            ("Rasa Server", self.test_rasa_server),
            ("Action Server", self.test_action_server),
            ("Integration Server", self.test_integration_server),
            ("ManVue API Connection", self.test_manvue_api),
            ("Chat Functionality", self.test_chat_functionality),
            ("Product Search", self.test_product_search),
            ("Frontend Assets", self.test_frontend_assets),
            ("Widget Integration", self.test_widget_integration)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing {test_name}...")
            try:
                result = test_func()
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{status} {test_name}")
                self.test_results.append((test_name, result))
            except Exception as e:
                print(f"❌ FAIL {test_name}: {e}")
                self.test_results.append((test_name, False))
        
        self.print_summary()
        
    def test_rasa_server(self):
        """Test Rasa server connectivity"""
        try:
            response = requests.get(f"{self.rasa_url}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_action_server(self):
        """Test action server connectivity"""
        try:
            # Actions server doesn't have a status endpoint, so we'll test webhook
            response = requests.post(
                f"{self.action_url}/webhook",
                json={"next_action": "action_listen"},
                timeout=5
            )
            return response.status_code in [200, 404, 422]  # Various acceptable responses
        except:
            return False
    
    def test_integration_server(self):
        """Test integration server"""
        try:
            response = requests.get(f"{self.integration_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_manvue_api(self):
        """Test ManVue API connectivity"""
        try:
            response = requests.get(f"{self.manvue_api_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_chat_functionality(self):
        """Test basic chat functionality"""
        try:
            message = {
                "sender": "test_user",
                "message": "hello"
            }
            
            response = requests.post(
                f"{self.rasa_url}/webhooks/rest/webhook",
                json=message,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return len(data) > 0 and 'text' in data[0]
            return False
        except:
            return False
    
    def test_product_search(self):
        """Test product search functionality"""
        try:
            message = {
                "sender": "test_user",
                "message": "show me t-shirts"
            }
            
            response = requests.post(
                f"{self.rasa_url}/webhooks/rest/webhook",
                json=message,
                timeout=10
            )
            
            return response.status_code == 200
        except:
            return False
    
    def test_frontend_assets(self):
        """Test frontend assets availability"""
        try:
            assets = [
                "/static/chatbot.html",
                "/static/chatbot.css",
                "/static/chatbot.js",
                "/static/chatbot_widget.js"
            ]
            
            for asset in assets:
                response = requests.get(f"{self.integration_url}{asset}", timeout=5)
                if response.status_code != 200:
                    print(f"   ❌ Asset not found: {asset}")
                    return False
            
            return True
        except:
            return False
    
    def test_widget_integration(self):
        """Test widget integration script"""
        try:
            widget_file = Path(__file__).parent / "chatbot_widget.js"
            return widget_file.exists() and widget_file.stat().st_size > 1000
        except:
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")
        
        print(f"\n📈 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Chatbot is ready to use.")
            self.print_usage_instructions()
        else:
            print("⚠️ Some tests failed. Check the services and try again.")
            self.print_troubleshooting()
    
    def print_usage_instructions(self):
        """Print usage instructions"""
        print("\n" + "🚀 How to Use Your Chatbot")
        print("-" * 30)
        print("1. 💻 Direct Access: http://localhost:5055")
        print("2. 🌐 ManVue Integration: Already added to frontend/index.html")
        print("3. 🔌 WebSocket: ws://localhost:5055/ws")
        print("4. 📱 Widget: Include chatbot_widget.js in your pages")
        
    def print_troubleshooting(self):
        """Print troubleshooting tips"""
        print("\n" + "🔧 Troubleshooting")
        print("-" * 20)
        print("1. Ensure all services are running:")
        print("   - Rasa Server: rasa run --enable-api --cors '*' --port 5005")
        print("   - Action Server: rasa run actions --port 5055")
        print("   - Integration Server: python chatbot_server.py")
        print("2. Check if ManVue API is running on port 5000")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")
        print("4. Try restarting: python start_chatbot.py")

def main():
    """Main test runner"""
    tester = ChatbotTester()
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        test_methods = {
            'rasa': tester.test_rasa_server,
            'actions': tester.test_action_server,
            'integration': tester.test_integration_server,
            'manvue': tester.test_manvue_api,
            'chat': tester.test_chat_functionality,
            'search': tester.test_product_search,
            'frontend': tester.test_frontend_assets,
            'widget': tester.test_widget_integration
        }
        
        if test_name in test_methods:
            print(f"🧪 Running single test: {test_name}")
            result = test_methods[test_name]()
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.title()} test")
        else:
            print(f"❌ Unknown test: {test_name}")
            print(f"Available tests: {', '.join(test_methods.keys())}")
    else:
        tester.run_all_tests()

if __name__ == "__main__":
    main()

