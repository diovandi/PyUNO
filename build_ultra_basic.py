#!/usr/bin/env python3
"""
Ultra-basic diagnostic - test each component separately
"""

import sys
import os

def test_python_basic():
    """Test basic Python functionality"""
    print("=== BASIC PYTHON TEST ===")
    try:
        print(f"Python version: {sys.version}")
        print(f"Platform: {sys.platform}")
        print(f"Current directory: {os.getcwd()}")
        print("✓ Basic Python works")
        return True
    except Exception as e:
        print(f"❌ Basic Python failed: {e}")
        return False

def test_imports_individual():
    """Test each import individually"""
    print("\n=== INDIVIDUAL IMPORT TESTS ===")
    
    # Test sys imports
    try:
        import subprocess
        print("✓ subprocess import works")
    except Exception as e:
        print(f"❌ subprocess import failed: {e}")
        return False
    
    # Test pygame import
    try:
        import pygame
        print(f"✓ pygame import works: {pygame.version.ver}")
    except Exception as e:
        print(f"❌ pygame import failed: {e}")
        return False
    
    # Test PyInstaller import  
    try:
        import PyInstaller
        print(f"✓ PyInstaller import works: {PyInstaller.__version__}")
    except Exception as e:
        print(f"❌ PyInstaller import failed: {e}")
        return False
    
    return True

def test_file_access():
    """Test file system access"""
    print("\n=== FILE SYSTEM TEST ===")
    try:
        # Test current directory
        files = os.listdir('.')
        print(f"✓ Current directory has {len(files)} items")
        
        # Test main_game.py specifically
        if os.path.exists('main_game.py'):
            size = os.path.getsize('main_game.py')
            print(f"✓ main_game.py exists ({size} bytes)")
        else:
            print("❌ main_game.py not found")
            return False
            
        # Test assets directory
        if os.path.exists('assets'):
            asset_files = os.listdir('assets')
            print(f"✓ assets directory has {len(asset_files)} files")
        else:
            print("❌ assets directory not found")
            return False
            
        return True
    except Exception as e:
        print(f"❌ File system test failed: {e}")
        return False

def test_subprocess_basic():
    """Test basic subprocess functionality"""
    print("\n=== SUBPROCESS TEST ===")
    try:
        import subprocess
        # Test basic python command
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ Subprocess python --version works: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Subprocess failed: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Subprocess test failed: {e}")
        return False

def test_pyinstaller_executable():
    """Test if PyInstaller executable works"""
    print("\n=== PYINSTALLER EXECUTABLE TEST ===")
    try:
        import subprocess
        # Test PyInstaller version command
        result = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ PyInstaller --version works: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ PyInstaller --version failed: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ PyInstaller executable test failed: {e}")
        return False

def main():
    """Run ultra-basic tests to isolate Windows CI issues"""
    print("🔬 ULTRA-BASIC WINDOWS CI DIAGNOSTIC")
    print("=" * 60)
    
    tests = [
        ("Basic Python", test_python_basic),
        ("Individual Imports", test_imports_individual), 
        ("File System Access", test_file_access),
        ("Subprocess Basic", test_subprocess_basic),
        ("PyInstaller Executable", test_pyinstaller_executable),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: CRASHED - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("The issue is likely in our build scripts, not the environment.")
    else:
        print("\n💥 SOME TESTS FAILED!")
        print("This indicates a Windows CI environment issue.")
        
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        print(f"\nExiting with code: {0 if success else 1}")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 SCRIPT CRASHED: {e}")
        sys.exit(1) 