@echo off
REM Build with cx_Freeze - alternative to PyInstaller

echo Building SQLite Manager with cx_Freeze...
echo.

call venv\Scripts\activate.bat

REM Install cx_Freeze
pip install cx_Freeze --quiet

REM Build
python setup.py build

echo.
if exist "build\exe.win-amd64-3.10\SQLiteManager.exe" (
    echo.
    echo =====================================================
    echo Build SUCCESSFUL!
    echo =====================================================
    echo.
    echo Executable: build\exe.win-amd64-3.10\SQLiteManager.exe
    echo.
    echo You can copy the entire build\exe.win-amd64-3.10\ folder
    echo to distribute the application
    echo.
) else (
    echo Build may have failed or output in different directory
    dir /s build\*.exe
)

pause
