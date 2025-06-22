#!/usr/bin/env python3
"""
Windows-specific debug script to isolate CI issues
"""

import os
import sys
import subprocess
import platform

def test_basic_environment():
    """Test basic Python environment"""
    print("=== Basic Environment Test ===")
    print(f"Platform: {platform.system()}")
    print(f"Platform release: {platform.release()}")
    print(f"Platform version: {platform.version()}")
    print(f"Python: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    print("\n--- File System Check ---")
    print("Current directory contents:")
    for item in sorted(os.listdir('.')):
        path = os.path.join('.', item)
        if os.path.isdir(path):
            try:
                size = len(os.listdir(path))
                print(f"  📁 {item}/ ({size} items)")
            except PermissionError:
                print(f"  📁 {item}/ (permission denied)")
        else:
            try:
                size = os.path.getsize(path)
                print(f"  📄 {item} ({size:,} bytes)")
            except OSError as e:
                print(f"  📄 {item} (error: {e})")

def test_python_imports():
    """Test critical Python imports"""
    print("\n=== Python Import Test ===")
    
    # Test pygame
    try:
        import pygame
        print(f"✓ pygame {pygame.version.ver} imported successfully")
        print(f"  Location: {pygame.__file__}")
        
        # Test pygame initialization
        try:
            pygame.mixer.pre_init()
            pygame.mixer.quit()
            print("✓ pygame mixer test passed")
        except Exception as e:
            print(f"⚠️  pygame mixer test failed: {e}")
            
    except ImportError as e:
        print(f"❌ pygame import failed: {e}")
        return False
    
    # Test PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} imported successfully")
        print(f"  Location: {PyInstaller.__file__}")
    except ImportError as e:
        print(f"❌ PyInstaller import failed: {e}")
        return False
    
    return True

def test_pyinstaller_basic():
    """Test basic PyInstaller functionality"""
    print("\n=== PyInstaller Basic Test ===")
    
    # Test PyInstaller help
    try:
        result = subprocess.run([sys.executable, "-m", "PyInstaller", "--help"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✓ PyInstaller help command works")
        else:
            print(f"❌ PyInstaller help failed: {result.returncode}")
            print(f"Stderr: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ PyInstaller help command timed out")
        return False
    except Exception as e:
        print(f"❌ PyInstaller help error: {e}")
        return False
    
    return True

def test_ultra_minimal_build():
    """Test the most minimal possible PyInstaller build"""
    print("\n=== Ultra-Minimal Build Test ===")
    
    if not os.path.exists("main_game.py"):
        print("❌ main_game.py not found")
        return False
    
    # Absolute minimal command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--distpath", "dist_debug_windows",
        "--workpath", "build_debug_windows", 
        "--specpath", ".",
        "--noconfirm",
        "--log-level", "DEBUG",
        "main_game.py"
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print("This is the absolute minimum PyInstaller command with debug logging")
    
    try:
        print("\nStarting PyInstaller...")
        result = subprocess.run(cmd, text=True, timeout=300)  # 5 minute timeout
        
        print(f"\nPyInstaller completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            print("✓ PyInstaller succeeded!")
            
            # Check output
            exe_path = "dist_debug_windows/main_game.exe"
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path)
                print(f"✓ Created: {exe_path} ({size:,} bytes)")
                return True
            else:
                print("❌ Expected executable not found")
                # List what was created
                try:
                    files = os.listdir("dist_debug_windows")
                    print(f"Files in dist_debug_windows: {files}")
                except FileNotFoundError:
                    print("dist_debug_windows directory not created")
                return False
        else:
            print(f"❌ PyInstaller failed with return code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ PyInstaller timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ PyInstaller error: {e}")
        return False

def main():
    """Run all Windows debug tests"""
    print("🔍 Windows CI Debug Script")
    print("=" * 50)
    
    success = True
    
    test_basic_environment()
    
    if not test_python_imports():
        success = False
    
    if not test_pyinstaller_basic():
        success = False
    
    if not test_ultra_minimal_build():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All Windows debug tests PASSED!")
        print("The issue may be in our more complex build scripts.")
    else:
        print("💥 Windows debug tests FAILED!")
        print("This indicates a fundamental CI environment issue.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 