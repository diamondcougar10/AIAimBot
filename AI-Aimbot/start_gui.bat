@echo off
cd /d "%~dp0"

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Virtual environment found. Starting AI Aimbot GUI...
    call .venv\Scripts\activate.bat
    python gui.py
) else (
    echo ==========================================
    echo   First-Time Setup Required
    echo ==========================================
    echo.
    echo Virtual environment not found.
    echo Running automatic setup...
    echo.
    
    REM Run setup
    call setup_internal.bat
    
    if exist ".venv\Scripts\python.exe" (
        echo.
        echo Setup complete! Starting AI Aimbot GUI...
        call .venv\Scripts\activate.bat
        python gui.py
    ) else (
        echo.
        echo ERROR: Setup failed. Please check the errors above.
        pause
    )
)
