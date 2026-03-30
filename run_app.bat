@echo off
REM Western Air Compliance - Desktop PDF Application Launcher
REM This batch file launches the Desktop PDF Report Generator

echo ==========================================
echo Western Air Compliance PDF Report Generator
echo Desktop Application Launcher
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found...

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import tkinter, pypdf, reportlab" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Dependencies OK...
echo.
echo Starting Desktop PDF Application...
echo.

REM Launch the application
python desktop_pdf_app.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
