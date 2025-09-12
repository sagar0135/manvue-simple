#!/bin/bash

# ManVue Chatbot Startup Script for Unix/Linux/Mac

echo "=============================================="
echo "🤖 ManVue Fashion Chatbot Startup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python not found! Please install Python 3.8 or higher."
        echo "📥 Visit: https://www.python.org/downloads/"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_status "Python found: $($PYTHON_CMD --version)"

# Check if we're in the correct directory
if [ ! -f "config.yml" ]; then
    print_error "config.yml not found!"
    print_info "Make sure you're running this from the chatbot directory."
    exit 1
fi

print_status "Current directory: $(pwd)"

# Make the script executable if it isn't already
chmod +x "$0"

# Install/upgrade dependencies
echo
print_info "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies"
    exit 1
fi

print_status "Dependencies installed"

# Check if virtual environment is recommended
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Not running in a virtual environment"
    print_info "Consider using: python3 -m venv venv && source venv/bin/activate"
fi

# Start the chatbot system
echo
print_info "🚀 Starting ManVue Chatbot System..."
$PYTHON_CMD start_chatbot.py

echo
print_info "👋 Chatbot system stopped."

