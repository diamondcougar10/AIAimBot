@echo off
cd /d "%~dp0"
echo ==========================================
echo      AI Aimbot - First Time Setup
echo ==========================================
echo.

REM Find Python
set "PYTHON_CMD=python"
python --version >nul 2>&1
if %errorlevel% equ 0 goto :FoundPython

echo 'python' command not found. Checking specific paths...
if exist "C:\Users\curph\AppData\Local\Programs\Python\Python311\python.exe" (
    set "PYTHON_CMD=C:\Users\curph\AppData\Local\Programs\Python\Python311\python.exe"
    goto :FoundPython
)
if exist "C:\Users\curph\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=C:\Users\curph\AppData\Local\Programs\Python\Python312\python.exe"
    goto :FoundPython
)

echo.
echo ERROR: Python not found.
echo Please install Python 3.11 or 3.12 from python.org
pause
exit /b 1

:FoundPython
echo Python found: %PYTHON_CMD%
echo.

REM Remove old venv if it exists
if exist ".venv" (
    echo Removing old virtual environment...
    rmdir /s /q .venv
)

echo Creating virtual environment...
"%PYTHON_CMD%" -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.
echo.

echo.
echo Environment 'RootKit' is active.
echo Installing basic requirements from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install requirements.
    echo Please check your internet connection or try running as administrator.
    pause
    exit /b
)

echo.
echo ==========================================
echo      GPU Selection
echo ==========================================
echo Do you have an NVIDIA GPU? (y/n)
set /p use_nvidia="> "

if /i "%use_nvidia%"=="y" (
    echo.
    echo Installing PyTorch for NVIDIA GPU - CUDA 11.8...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
) else (
    echo.
    echo Installing PyTorch for CPU/AMD...
    pip install torch torchvision torchaudio
)

echo.
echo ==========================================
echo Setup complete! 
echo You can now run the bot using 'run.bat'.
echo ==========================================
pause
