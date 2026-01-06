@echo off
echo ========================================
echo NED University Document Management
echo Starting Backend Server
echo ========================================
echo.

REM Navigate to server directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if FastAPI is installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: FastAPI not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Copying from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your settings
    echo Press any key to continue...
    pause >nul
)

echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

REM Start the server
python main.py

pause
