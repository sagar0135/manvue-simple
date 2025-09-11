#!/bin/bash

echo "================================"
echo "MANVUE Image Setup for Unix/Linux"
echo "================================"
echo

echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi
echo "✓ Python is available"

echo
echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo
echo "[3/4] Starting MongoDB image setup..."
echo "This will download images and store them in your MongoDB database..."
python3 setup_manvue_images.py
if [ $? -ne 0 ]; then
    echo "ERROR: Setup failed - check the output above"
    exit 1
fi

echo
echo "[4/4] Setup completed!"
echo "✓ Images converted to GridFS"
echo "✓ Products seeded in database"
echo "✓ API ready to serve images"
echo
echo "Next steps:"
echo "1. Start your API server: python3 ../start_enhanced_backend.py"
echo "2. Test the API: http://localhost:5001/api/products"
echo "3. Update your frontend with the new product IDs"
echo
