#!/bin/bash

echo "========================================"
echo "University Document Management System"
echo "Backend Setup Script (Linux/Mac)"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from your package manager"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Try manually: pip install -r requirements.txt"
    exit 1
fi

echo "[4/5] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - PLEASE EDIT IT with your settings!"
else
    echo ".env file already exists"
fi

echo "[5/5] Checking Tesseract installation..."
if ! command -v tesseract &> /dev/null; then
    echo "WARNING: Tesseract OCR is not installed"
    echo "Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "MacOS: brew install tesseract"
    echo "OCR features will not work without it"
else
    echo "Tesseract OCR found!"
    tesseract --version
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Create database: createdb university_docs"
echo "3. Run: source venv/bin/activate && python main.py"
echo ""
