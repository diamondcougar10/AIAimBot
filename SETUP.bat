@echo off
echo ========================================
echo   AI Aimbot - Automatic Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11 or newer from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo [1/4] Python found - checking version...
python --version

echo.
echo [2/4] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo [3/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/4] Installing dependencies (this may take 5-10 minutes)...
echo This will install PyTorch, CUDA support, OpenCV, and other requirements.
echo.

cd AI-Aimbot
python -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To run the AI Aimbot:
echo   1. Double-click RUN_AIMBOT.bat
echo.
echo Or run manually:
echo   .venv\Scripts\activate
echo   cd AI-Aimbot
echo   python gui.py
echo.
pause
