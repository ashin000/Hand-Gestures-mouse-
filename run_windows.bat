@echo off
title Virtual Mouse - Hand Gesture Control
cd /d "%~dp0"

echo ==========================================
echo      VIRTUAL MOUSE - HAND GESTURES
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
echo ERROR: Virtual environment not found!
echo Please check that the .venv folder exists.
pause
exit /b 1
)

echo Starting Virtual Mouse...
echo Move your index finger to move the cursor.
echo Pinch your thumb and index finger to click.
echo Press Q in the camera window to exit.
echo.

".venv\Scripts\python.exe" main.py

if errorlevel 1 (
echo.
echo The application stopped because of an error.
pause
)
