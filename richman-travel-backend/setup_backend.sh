#!/bin/bash
# Complete setup script for Richman Travel Backend

set -e

echo "🚀 Setting up Richman Travel Backend..."

# First, let's fix the permissions and create proper directory structure
echo "📁 Setting up directory structure..."

# Make sure we're in the backend directory
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Error: Please run this script from the richman-travel-backend directory"
    exit 1
fi

# Fix the calendar service filename if it exists
if [[ -f "app/services/calender_service.py" ]]; then
    echo "📝 Fixing calendar service filename..."
    mv app/services/calender_service.py app/services/calendar_service.py
    echo "✅ Renamed calender_service.py to calendar_service.py"
fi

# Create virtual environment using pyenv
echo "🐍 Creating virtual environment with Python 3.8.13..."
if [[ ! -d "venv" ]]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
