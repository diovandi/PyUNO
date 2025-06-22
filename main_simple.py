#!/usr/bin/env python3
"""
Simple test program without pygame dependencies
For testing Windows CI PyInstaller functionality
"""

import sys
import os

def main():
    print("🎮 Simple PyUNO Test Program")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Current directory: {os.getcwd()}")
    
    print("\nThis is a simple test program to verify:")
    print("1. Python execution works")
    print("2. PyInstaller can create executables")
    print("3. Basic file operations work")
    
    # Test file operations
    try:
        files = os.listdir('.')
        print(f"\nCurrent directory contains {len(files)} files")
        
        # Look for assets
        if os.path.exists('assets'):
            assets = os.listdir('assets')
            print(f"Assets directory contains {len(assets)} files")
        else:
            print("No assets directory found")
            
    except Exception as e:
        print(f"Error accessing files: {e}")
    
    print("\n🎉 Simple test completed successfully!")
    print("If you see this message, the executable works!")
    
    # Keep window open briefly
    try:
        input("\nPress Enter to exit...")
    except EOFError:
        # Handle case where input is not available (CI environment)
        import time
        time.sleep(2)

if __name__ == "__main__":
    main() 