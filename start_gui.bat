@echo off
REM Launcher for Kid-Friendly Vocabulary Trainer GUI
REM Double-click this file to start the app!

title Vocabulary Trainer - Starting...

echo.
echo ========================================
echo    Starting Vocabulary Trainer! 
echo    Please wait...
echo ========================================
echo.

python gui.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo    Oops! Something went wrong.
    echo    Make sure Python is installed!
    echo ========================================
    echo.
    pause
)
