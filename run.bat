@echo off
echo ====================================
echo Hospital Management System - Backend
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\fastapi\" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create .env file from .env.example
    echo.
    pause
    exit
)

echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python main.py






