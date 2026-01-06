@echo off
echo ============================================
echo Database Setup for Document Reader
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    echo.
) else (
    call venv\Scripts\activate
)

echo Running database setup script...
echo.
python setup_database.py

echo.
pause
