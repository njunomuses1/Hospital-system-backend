#!/bin/bash

echo "===================================="
echo "Hospital Management System - Backend"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if requirements are installed
if [ ! -f "venv/lib/python*/site-packages/fastapi/__init__.py" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please create .env file from .env.example"
    echo ""
    exit 1
fi

echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

python main.py






