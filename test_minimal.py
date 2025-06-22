#!/usr/bin/env python3
"""
Absolute minimal test - just test if Python execution works
"""

print("🔬 MINIMAL PYTHON TEST")
print("If you see this, Python execution works")

try:
    import sys
    print(f"✓ Python version: {sys.version}")
    print(f"✓ Platform: {sys.platform}")
except Exception as e:
    print(f"❌ Basic sys import failed: {e}")
    exit(1)

try:
    import os
    print(f"✓ Current directory: {os.getcwd()}")
    files = os.listdir('.')
    print(f"✓ Directory has {len(files)} items")
except Exception as e:
    print(f"❌ Basic os operations failed: {e}")
    exit(1)

print("🎉 ALL MINIMAL TESTS PASSED!")
print("The issue is likely in more complex imports or operations")
exit(0) 