@echo off
REM Simple launcher for SQLite Manager

echo Starting SQLite Manager...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py
