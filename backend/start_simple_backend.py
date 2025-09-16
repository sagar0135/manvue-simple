#!/usr/bin/env python3
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Start the simple backend
import uvicorn
from backend.simple_main import app

if __name__ == "__main__":
    print("Starting ManVue Simple Backend on http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
