#!/usr/bin/env python3
"""
Test script for product page functionality
"""
import requests
import webbrowser
import time
import subprocess
import sys
import os

def test_backend():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend not responding properly")
            return False
    except requests.exceptions.RequestException:
        print("❌ Backend not running")
        return False

def test_product_endpoint():
    """Test individual product endpoint"""
    try:
        response = requests.get("http://localhost:5000/products/1", timeout=5)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product endpoint working - Found: {product.get('title', 'Unknown')}")
            return True
        else:
            print("❌ Product endpoint failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Product endpoint error: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    try:
        # Start backend in background
        subprocess.Popen([
            sys.executable, "api/enhanced_main.py"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(30):
            if test_backend():
                return True
            time.sleep(1)
            print(f"   Attempt {i+1}/30...")
        
        print("❌ Backend failed to start within timeout")
        return False
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def start_frontend():
    """Start the frontend server"""
    print("🎨 Starting frontend server...")
    try:
        # Change to frontend directory
        os.chdir("frontend")
        
        # Start HTTP server
        subprocess.Popen([
            sys.executable, "-m", "http.server", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ Frontend server started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

def open_product_page():
    """Open the product page in browser"""
    print("🌐 Opening product page...")
    time.sleep(2)  # Give servers time to start
    
    # Open main page first
    webbrowser.open("http://localhost:8000")
    
    # Then open product page
    time.sleep(1)
    webbrowser.open("http://localhost:8000/product.html?id=1")
    
    print("✅ Product page opened in browser")

def main():
    print("🧪 MANVUE PRODUCT PAGE TEST")
    print("=" * 50)
    
    # Test if backend is already running
    if not test_backend():
        print("🔄 Backend not running, starting it...")
        if not start_backend():
            print("❌ Failed to start backend. Exiting.")
            return
    
    # Test product endpoint
    if not test_product_endpoint():
        print("❌ Product endpoint test failed. Exiting.")
        return
    
    # Start frontend
    if not start_frontend():
        print("❌ Failed to start frontend. Exiting.")
        return
    
    # Open product page
    open_product_page()
    
    print("\n🎉 Product page test completed!")
    print("📋 What to test:")
    print("   1. Product details are displayed correctly")
    print("   2. Size and color options work")
    print("   3. Quantity controls function")
    print("   4. Add to cart works")
    print("   5. AI recommendations are shown")
    print("   6. Image zoom works")
    print("   7. Reviews are displayed")
    print("\n🛑 Press Ctrl+C to stop servers")

if __name__ == "__main__":
    try:
        main()
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Test stopped by user")
        print("✅ All servers should be running in background")
