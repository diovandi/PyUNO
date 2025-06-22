#!/usr/bin/env python3
"""
Simple build script that mirrors the working local build
"""

import os
import sys
import subprocess
import platform

def main():
    """Simple build that works locally"""
    
    print("=== Simple PyUNO Build ===")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    
    # Check if we have the basics
    try:
        import pygame
        print(f"✓ pygame: {pygame.version.ver}")
    except ImportError:
        print("❌ pygame not found")
        return False
        
    try:
        import PyInstaller
        print(f"✓ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Simple build command (like the local one that worked)
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "PyUNO_Final",
        "--add-data", "assets;assets" if platform.system() == "Windows" else "assets:assets",
        "--collect-all", "pygame",
        "--distpath", "dist_final",
        "--noconfirm",
        "main_game.py"
    ]
    
    # Add icon if available
    icon_file = None
    if platform.system() == "Windows" and os.path.exists("assets/uno_logo.ico"):
        icon_file = "assets/uno_logo.ico"
    elif os.path.exists("assets/uno_logo.png"):
        icon_file = "assets/uno_logo.png"
    
    if icon_file:
        cmd.extend(["--icon", icon_file])
        print(f"✓ Using icon: {icon_file}")
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build successful!")
        
        # Check what was created
        if platform.system() == "Windows":
            exe_path = "dist_final/PyUNO_Final.exe"
        elif platform.system() == "Darwin":
            exe_path = "dist_final/PyUNO_Final.app"
        else:
            exe_path = "dist_final/PyUNO_Final"
            
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) if os.path.isfile(exe_path) else "N/A"
            print(f"✓ Created: {exe_path} ({size} bytes)")
            return True
        else:
            print(f"❌ Expected file not found: {exe_path}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 