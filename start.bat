@echo off
title AI Real Estate Explorer
echo.
echo  ============================================
echo    AI Real Estate Explorer - Starting...
echo  ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Install dependencies
echo  [1/3] Installing dependencies...
pip install -r backend\requirements.txt -q
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo        Done.
echo.

:: Create .env if missing
if not exist backend\.env (
    echo  [2/3] Creating .env from example...
    if exist backend\.env.example (
        copy backend\.env.example backend\.env >nul
    ) else (
        echo LLM_PROVIDER=openai> backend\.env
        echo OPENAI_API_KEY=>> backend\.env
        echo MODEL_NAME=gpt-4o-mini>> backend\.env
    )
    echo        Created backend\.env - add your API key there for AI features.
) else (
    echo  [2/3] .env already exists - skipping.
)
echo.

:: Start server + open browser
echo  [3/3] Starting server on http://localhost:8000
echo.
echo  ============================================
echo    Backend API:  http://localhost:8000/docs
echo    Frontend:     http://localhost:8000/app
echo  ============================================
echo.
echo  Press Ctrl+C to stop the server.
echo.

:: Open browser after 2 sec delay (non-blocking)
start /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8000/app"

:: Run server
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
