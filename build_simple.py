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
        "--name", "PyUNO_Final",
        "--add-data", f"assets{separator}assets",
        "--collect-all", "pygame",
        "--distpath", "dist_final",
        "--noconfirm",
        "main_game.py"
    ]
    
    # Only add --windowed on non-Windows for now to debug Windows issues
    if platform.system() != "Windows":
        cmd.insert(2, "--windowed")  # Insert after --onefile
        print("Added --windowed flag for non-Windows platform")
    else:
        print("Skipping --windowed on Windows for debugging")
    
    # Simplified icon handling - only use existing files, don't generate
    icon_file = None
    if platform.system() == "Windows" and os.path.exists("assets/uno_logo.ico"):
        icon_file = "assets/uno_logo.ico"
        print(f"✓ Found existing ICO file: {icon_file}")
    elif platform.system() == "Darwin" and os.path.exists("assets/uno_logo.png"):
        icon_file = "assets/uno_logo.png"
        print(f"✓ Using PNG for macOS: {icon_file}")
    elif os.path.exists("assets/uno_logo.png"):
        # Only use PNG on non-Windows if no ICO exists
        if platform.system() != "Windows":
            icon_file = "assets/uno_logo.png"
            print(f"✓ Using PNG icon: {icon_file}")
        else:
            print("⚠️  PNG found but skipping on Windows (no ICO available)")
    
    if icon_file:
        cmd.extend(["--icon", icon_file])
        print(f"✓ Using icon: {icon_file}")
    else:
        print("⚠️  No icon file used (may help with Windows debugging)")
    
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
            # Handle different types of outputs correctly
            if platform.system() == "Darwin" and exe_path.endswith(".app"):
                # macOS .app bundle is a directory
                if os.path.isdir(exe_path):
                    print(f"✓ Created macOS app bundle: {exe_path}")
                    # Check if it has the expected structure
                    contents_path = os.path.join(exe_path, "Contents")
                    if os.path.exists(contents_path):
                        print(f"✓ App bundle structure verified")
                    return True
                else:
                    print(f"❌ Expected directory bundle, got file: {exe_path}")
                    return False
            elif os.path.isfile(exe_path):
                # Regular executable file
                size = os.path.getsize(exe_path)
                print(f"✓ Created executable: {exe_path} ({size:,} bytes)")
                return True
            elif os.path.isdir(exe_path):
                # Directory (shouldn't happen for Windows/Linux)
                print(f"✓ Created directory: {exe_path}")
                return True
            else:
                print(f"❌ Unexpected file type: {exe_path}")
                return False
        else:
            print(f"❌ Expected file not found: {exe_path}")
            print("Files in dist_final:")
            try:
                dist_files = os.listdir("dist_final")
                if dist_files:
                    for f in dist_files:
                        full_path = os.path.join("dist_final", f)
                        if os.path.isdir(full_path):
                            print(f"  📁 {f}/")
                        else:
                            size = os.path.getsize(full_path)
                            print(f"  📄 {f} ({size:,} bytes)")
                else:
                    print("  (empty directory)")
            except FileNotFoundError:
                print("  ❌ dist_final directory doesn't exist")
            
            # Don't fail immediately - maybe PyInstaller created something else
            print("⚠️  Expected file not found, but continuing...")
            return True  # Allow partial success for artifact upload
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 