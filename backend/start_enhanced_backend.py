#!/usr/bin/env python3
"""
Enhanced ManVue Backend with ML Search Capabilities
"""
import sys
import os
import uvicorn

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from enhanced_main import app
    print("🚀 Starting ManVue Enhanced Backend Server...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("🤖 ML Features Enabled:")
    print("   - AI-powered text search")
    print("   - Image-based product search")
    print("   - ML integration with fashion recognition")
    print("\n📋 Enhanced API Endpoints:")
    print("   - GET  /                    - Health check & API info")
    print("   - GET  /products            - Get all products")
    print("   - POST /products            - Add new product")
    print("   - POST /products/search     - AI text search")
    print("   - POST /products/image-search - AI image search")
    print("   - GET  /ml/health           - ML service status")
    print("   - POST /register            - User registration")
    print("   - POST /login               - User login")
    print("   - GET  /products/category/{category} - Category filter")
    print("\n🔄 Starting enhanced server...")
    
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
    
except ImportError as e:
    print(f"❌ Error importing enhanced backend: {e}")
    print("Make sure you're in the project root directory")
except Exception as e:
    print(f"❌ Error starting enhanced server: {e}")
