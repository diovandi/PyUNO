#!/usr/bin/env python3
"""
Build script for creating PyUNO executable
Cross-platform support for Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def get_platform_info():
    """Get platform-specific information"""
    system = platform.system().lower()
    
    if system == "windows":
        return {
            "name": "Windows",
            "executable_name": "PyUNO.exe",
            "data_separator": ";",
            "icon_ext": ".ico",
            "launcher_ext": ".bat"
        }
    elif system == "darwin":
        return {
            "name": "macOS", 
            "executable_name": "PyUNO.app",
            "data_separator": ":",
            "icon_ext": ".icns",
            "launcher_ext": ".command"
        }
    else:  # Linux and others
        return {
            "name": "Linux",
            "executable_name": "PyUNO",
            "data_separator": ":",
            "icon_ext": ".png", 
            "launcher_ext": ".sh"
        }

def create_launcher_script(script_dir, platform_info):
    """Create a platform-specific launcher script"""
    launcher_name = f"run_pyuno{platform_info['launcher_ext']}"
    launcher_path = script_dir / "dist" / launcher_name
    
    if platform_info['name'] == "Windows":
        # Windows batch file
        content = '''@echo off
echo Starting PyUNO...
cd /d "%~dp0"
PyUNO.exe
pause
'''
    elif platform_info['name'] == "macOS":
        # macOS command file
        content = '''#!/bin/bash
echo "Starting PyUNO..."
cd "$(dirname "$0")"
open PyUNO.app
'''
    else:
        # Linux shell script
        content = '''#!/bin/bash
echo "Starting PyUNO..."
cd "$(dirname "$0")"
./PyUNO
'''
    
    with open(launcher_path, "w") as f:
        f.write(content)
    
    # Make executable on Unix-like systems
    if platform_info['name'] in ["macOS", "Linux"]:
        os.chmod(launcher_path, 0o755)

def create_executable():
    """Create the PyUNO executable using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Get platform info
    platform_info = get_platform_info()
    print(f"Building for {platform_info['name']}...")
    
    # Define paths
    script_dir = Path(__file__).parent
    main_script = script_dir / "main_game.py"
    assets_dir = script_dir / "assets"
    src_dir = script_dir / "src"
    
    # Find appropriate icon file
    icon_file = None
    possible_icons = [
        assets_dir / f"uno_logo{platform_info['icon_ext']}",
        assets_dir / "uno_logo.png",
        assets_dir / "uno_logo.ico",
        assets_dir / "uno_logo.icns"
    ]
    
    for icon_path in possible_icons:
        if icon_path.exists():
            icon_file = str(icon_path)
            break
    
    # PyInstaller command
    separator = platform_info['data_separator']
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Hide console window (for GUI apps)
        "--name", "PyUNO",  # Name of the executable
        f"--add-data={assets_dir}{separator}assets",  # Include assets folder
        f"--add-data={src_dir}{separator}src",  # Include source folder
        "--distpath", "dist",  # Output directory
        "--workpath", "build",  # Temporary build directory
        "--specpath", ".",  # Where to put the .spec file
        str(main_script)
    ]
    
    # Add icon if found
    if icon_file:
        cmd.extend(["--icon", icon_file])
    
    # macOS specific options
    if platform_info['name'] == "macOS":
        cmd.extend([
            "--osx-bundle-identifier", "com.pyuno.game",
            "--target-arch", "universal2"  # Support both Intel and Apple Silicon
        ])
    
    print("Building PyUNO executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        
        executable_path = script_dir / "dist" / platform_info["executable_name"]
        print(f"Executable created at: {executable_path}")
        
        # Create platform-specific launcher script
        create_launcher_script(script_dir, platform_info)
        
        print(f"Also created launcher script for easy execution")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True

def clean_build():
    """Clean build artifacts"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["PyUNO.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            print(f"Cleaning {file_name}...")
            os.remove(file_name)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build PyUNO executable")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    parser.add_argument("--rebuild", action="store_true", help="Clean and rebuild")
    
    args = parser.parse_args()
    
    if args.clean or args.rebuild:
        clean_build()
    
    if not args.clean:
        success = create_executable()
        if success:
            print("\n" + "="*50)
            print("PyUNO executable build completed!")
            print("Find your executable in the 'dist' folder")
            print("="*50)
        else:
            sys.exit(1) 