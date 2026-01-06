@echo off
echo ========================================
echo University Document Management System
echo Backend Setup Script (Windows)
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate

echo [3/5] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try manually: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - PLEASE EDIT IT with your settings!
) else (
    echo .env file already exists
)

echo [5/5] Checking Tesseract installation...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Tesseract OCR is not installed
    echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo OCR features will not work without it
) else (
    echo Tesseract OCR found!
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Create database: createdb university_docs
echo 3. Run: python main.py
echo.
pause
