#!/usr/bin/env python3
"""
Ultra-minimal build script to isolate CI issues
"""

import os
import sys
import subprocess
import platform

def main():
    """Ultra-minimal build - remove all potential issues"""
    
    print("=== Ultra-Minimal PyUNO Build ===")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    
    # Check basics
    try:
        import pygame
        print(f"✓ pygame: {pygame.version.ver}")
    except ImportError:
        print("❌ pygame not found")
        return False
    
    # Minimal PyInstaller command - remove ALL optional flags
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "PyUNO_Minimal",
        "--distpath", "dist_minimal",
        "--noconfirm",
        "main_game.py"
    ]
    
    print(f"Minimal command: {' '.join(cmd)}")
    print("Note: NO --windowed, NO --add-data, NO --collect-all, NO --icon")
    print("This should work if PyInstaller itself works")
    
    try:
        print("\nStarting minimal build...")
        result = subprocess.run(cmd, text=True, capture_output=False)
        
        if result.returncode == 0:
            print("✓ Minimal build completed!")
            
            # Check what was created
            if platform.system() == "Windows":
                exe_path = "dist_minimal/PyUNO_Minimal.exe"
            elif platform.system() == "Darwin":
                exe_path = "dist_minimal/PyUNO_Minimal.app"
            else:
                exe_path = "dist_minimal/PyUNO_Minimal"
            
            if os.path.exists(exe_path):
                if os.path.isfile(exe_path):
                    size = os.path.getsize(exe_path)
                    print(f"✓ Created minimal executable: {exe_path} ({size} bytes)")
                else:
                    print(f"✓ Created: {exe_path} (directory)")
                return True
            else:
                print(f"❌ Expected minimal executable not found: {exe_path}")
                return False
        else:
            print(f"❌ Minimal build failed with code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Minimal build SUCCESS! Now we can add features back...")
    else:
        print("\n💥 Even minimal build failed - this is a CI environment issue")
    sys.exit(0 if success else 1) 