#!/usr/bin/env python3
"""
Soutk Programming Language Test Suite
Runs all tests to verify language functionality
"""

import os
import sys
import subprocess
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_test(test_file, description):
    """Run a single test file"""
    print(f"🧪 Testing: {description}")
    print(f"   File: {test_file}")
    
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join('..', 'soutk.py'), 
            test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("   ✅ PASSED")
            return True
        else:
            print("   ❌ FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"   💥 ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Soutk Programming Language Test Suite")
    print("=" * 50)
    
    tests = [
        ("basic_syntax.stk", "Basic syntax and variables"),
        ("functions.stk", "Function definitions and calls"),
        ("classes.stk", "Object-oriented programming"),
        ("data_structures.stk", "Stacks, queues, linked lists"),
        ("file_operations.stk", "File I/O operations"),
        ("error_handling.stk", "Error handling with ward/rescue"),
        ("string_methods.stk", "String manipulation methods"),
        ("math_functions.stk", "Mathematical functions"),
        ("control_structures.stk", "Loops and conditionals"),
        ("comprehensive.stk", "All features combined")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        test_path = os.path.join("test_programs", test_file)
        if os.path.exists(test_path):
            if run_test(test_path, description):
                passed += 1
        else:
            print(f"⚠️  Test file not found: {test_path}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Soutk is working perfectly!")
        return 0
    else:
        print(f"❌ {total - passed} tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())