#!/bin/bash

# Face Recognition System - Quick Start Script
# Université de Saida - Dr. Moulay Tahar
# Master 2 RISR

echo "=========================================="
echo "  Face Recognition Cloud System"
echo "  Université de Saida - Dr. Moulay Tahar"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Create admin user if not exists
echo "👤 Creating admin user..."
python scripts/create_admin.py

# Start server
echo "🚀 Starting server..."
echo "📍 Access the application at:"
echo "   • Web UI: http://localhost:8000/static/index.html"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • Login: http://localhost:8000/static/login.html"
echo ""
echo "👤 Default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo "=========================================="

python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
