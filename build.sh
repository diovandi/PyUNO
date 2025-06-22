#!/bin/bash
echo "============================================"
echo "          PyUNO Executable Builder"
echo "============================================"
echo

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo
echo "Building executable..."
python3 build_executable.py

echo
echo "Build complete! Check the 'dist' folder for your executable"
echo

# Make the script executable
chmod +x dist/run_pyuno.command 2>/dev/null || chmod +x dist/run_pyuno.sh 2>/dev/null || true

echo "You can now run the game from the dist folder!"
read -p "Press Enter to continue..." 