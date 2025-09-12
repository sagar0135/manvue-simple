#!/usr/bin/env python3
"""
Simple backend startup script for ManVue
"""
import sys
import os
import uvicorn

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from simple_main import app
    print("🚀 Starting ManVue Backend Server...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("📋 API Endpoints:")
    print("   - GET  /              - Health check")
    print("   - GET  /products      - Get all products")
    print("   - POST /products      - Add new product")
    print("   - POST /register      - User registration")
    print("   - POST /login         - User login")
    print("   - GET  /products/category/{category} - Get products by category")
    print("\n🔄 Starting server...")
    
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
    
except ImportError as e:
    print(f"❌ Error importing backend: {e}")
    print("Make sure you're in the project root directory")
except Exception as e:
    print(f"❌ Error starting server: {e}")