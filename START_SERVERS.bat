@echo off
echo Starting Document Reader Application...
echo.

REM Check if virtual environment exists
if not exist "server\venv" (
    echo Creating Python virtual environment...
    cd server
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
    echo.
)

REM Start backend server in a new window
echo Starting Backend Server on http://localhost:8000
start "Backend Server" cmd /k "cd server && venv\Scripts\activate && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend server in a new window
echo Starting Frontend Server on http://localhost:3000
start "Frontend Server" cmd /k "cd client && npm run dev"

echo.
echo ============================================
echo Both servers are starting...
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo ============================================
echo.
echo Press any key to close this window (servers will keep running)
pause > nul
