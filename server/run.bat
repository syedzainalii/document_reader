@echo off
REM Activate virtual environment
call venv\Scripts\activate

REM Start FastAPI server
python main.py

pause
