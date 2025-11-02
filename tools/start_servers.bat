@echo off
echo ================================================
echo ATHLE TRACKER - Server Startup Script
echo ================================================
echo.

REM Kill all Python and Node processes
echo [1/4] Stopping all existing processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul
echo [OK] All processes stopped
echo.

REM Start FastAPI backend on port 8000
echo [2/4] Starting FastAPI backend on port 8000...
start "FastAPI Backend" cmd /k "cd /d "%~dp0" && venv\Scripts\python.exe -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 >nul
echo [OK] Backend started
echo.

REM Start Next.js frontend on port 3000
echo [3/4] Starting Next.js frontend on port 3000...
cd frontend
start "Next.js Frontend" cmd /k "npm run dev -- -p 3000"
cd ..
timeout /t 3 >nul
echo [OK] Frontend started
echo.

echo [4/4] Servers ready!
echo ================================================
echo.
echo FastAPI Backend:  http://localhost:8000
echo API Docs:         http://localhost:8000/docs
echo Next.js Frontend: http://localhost:3000
echo.
echo ================================================
echo Press any key to exit this window...
pause >nul
