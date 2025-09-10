#!/bin/bash

echo "========================================"
echo "    MANVUE API LAUNCHER (Unix/Linux/Mac)"
echo "========================================"
echo ""
echo "Starting ManVue API services..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Make the script executable
chmod +x "$0"

# Start the API launcher
$PYTHON_CMD launch_api.py
