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
    print(f"Current directory: {os.getcwd()}")
    
    # Check environment
    print("\n--- Environment Check ---")
    print(f"pygame in PATH: {'pygame' in sys.path}")
    print(f"Current working dir files:")
    for f in sorted(os.listdir('.')):
        if os.path.isdir(f):
            print(f"  📁 {f}/")
        else:
            print(f"  📄 {f}")
    
    print(f"\nAssets directory:")
    try:
        assets_files = os.listdir('assets')
        for f in sorted(assets_files)[:10]:  # Show first 10 files
            print(f"  - {f}")
        if len(assets_files) > 10:
            print(f"  ... and {len(assets_files) - 10} more files")
    except FileNotFoundError:
        print("  ❌ Assets directory not found!")
        return False
    
    # Check if we have the basics
    print("\n--- Dependencies ---")
    try:
        import pygame
        print(f"✓ pygame: {pygame.version.ver}")
        print(f"  pygame location: {pygame.__file__}")
    except ImportError:
        print("❌ pygame not found")
        return False
        
    try:
        import PyInstaller
        print(f"✓ PyInstaller: {PyInstaller.__version__}")
        print(f"  PyInstaller location: {PyInstaller.__file__}")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Simple build command (like the local one that worked)
    print("\n--- Build Configuration ---")
    separator = ";" if platform.system() == "Windows" else ":"
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "PyUNO_Final",
        "--add-data", f"assets{separator}assets",
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
    else:
        print("⚠️  No icon file found")
    
    print(f"Command: {' '.join(cmd)}")
    print(f"Data separator: '{separator}' for {platform.system()}")
    
    # Verify main_game.py exists
    if not os.path.exists("main_game.py"):
        print("❌ main_game.py not found!")
        return False
    else:
        print("✓ main_game.py found")
    
    try:
        # Run with real-time output to see exactly what happens
        print("Starting PyInstaller...")
        result = subprocess.run(cmd, text=True, capture_output=False)
        
        if result.returncode == 0:
            print("✓ PyInstaller completed successfully!")
        else:
            print(f"❌ PyInstaller failed with return code: {result.returncode}")
            return False
        
        # Check what was created
        if platform.system() == "Windows":
            exe_path = "dist_final/PyUNO_Final.exe"
        elif platform.system() == "Darwin":
            exe_path = "dist_final/PyUNO_Final.app"
        else:
            exe_path = "dist_final/PyUNO_Final"
            
        print(f"Checking for: {exe_path}")
        if os.path.exists(exe_path):
            if os.path.isfile(exe_path):
                size = os.path.getsize(exe_path)
                print(f"✓ Created: {exe_path} ({size} bytes)")
            else:
                print(f"✓ Created: {exe_path} (directory)")
            return True
        else:
            print(f"❌ Expected file not found: {exe_path}")
            print("Files in dist_final:")
            try:
                for f in os.listdir("dist_final"):
                    print(f"  - {f}")
            except FileNotFoundError:
                print("  dist_final directory doesn't exist")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 