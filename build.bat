@echo off
echo ============================================
echo          PyUNO Executable Builder
echo ============================================
echo.

echo Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Building executable...
python build_executable.py

echo.
echo Build complete! Check the 'dist' folder for PyUNO.exe
pause 