@echo off
echo ==========================================
echo   Building AI Aimbot Launcher
echo ==========================================
echo.

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run 'start_gui.bat' first to setup the environment.
    pause
    exit /b 1
)

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
python build_launcher.py

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo Build successful!
    echo.
    echo The launcher is in the 'dist' folder:
    echo   dist\AI_Aimbot_Launcher.exe
    echo.
    echo Distribution package contents:
    echo   - AI_Aimbot_Launcher.exe
    echo   - setup.bat
    echo   - All Python files and model files
    echo.
    echo Users run setup.bat once, then use the .exe
    echo ==========================================
) else (
    echo.
    echo ERROR: Build failed!
)

pause
