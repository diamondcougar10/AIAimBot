@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
cd AI-Aimbot
python gui.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start AI Aimbot!
    echo Did you run SETUP.bat first?
    pause
)
