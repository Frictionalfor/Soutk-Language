#!/usr/bin/env python3
"""
Soutk Programming Language - Main Entry Point
A magical programming language with unique syntax and powerful features.

Usage:
    python soutk.py program.stk
    python soutk.py --help
    python soutk.py --version
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from soutk_interpreter import SoutkInterpreter

def print_help():
    """Print help information"""
    print("""
🧙‍♂️ Soutk Programming Language

Usage:
    python soutk.py <program.stk>     Run a Soutk program
    python soutk.py --help           Show this help message
    python soutk.py --version        Show version information
    python soutk.py --examples       List available examples

Examples:
    python soutk.py examples/hello.stk
    python soutk.py examples/advanced_demo.stk
    python soutk.py my_program.stk

For more information, visit: https://github.com/yourusername/soutk
    """)

def print_version():
    """Print version information"""
    print("Soutk Programming Language v1.0.0")
    print("A magical programming language with unique syntax")

def list_examples():
    """List available example programs"""
    examples_dir = Path("examples")
    if examples_dir.exists():
        print("📚 Available Example Programs:")
        print("=" * 40)
        
        examples = sorted(examples_dir.glob("*.stk"))
        for example in examples:
            print(f"  • {example.name}")
        
        print("\nRun an example with:")
        print(f"  python soutk.py examples/{examples[0].name if examples else 'hello.stk'}")
    else:
        print("❌ Examples directory not found")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("❌ Error: No program file specified")
        print("Use 'python soutk.py --help' for usage information")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    # Handle command line options
    if arg == "--help" or arg == "-h":
        print_help()
        return
    elif arg == "--version" or arg == "-v":
        print_version()
        return
    elif arg == "--examples":
        list_examples()
        return
    
    # Run Soutk program
    filename = arg
    
    try:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"❌ Error: File '{filename}' not found.")
            sys.exit(1)
        
        with open(file_path, "r", encoding='utf-8') as f:
            code = f.read()
        
        print(f"🚀 Running Soutk program: {filename}")
        print("=" * 50)
        
        interpreter = SoutkInterpreter()
        interpreter.current_file = filename
        interpreter.execute(code)
        
        print("=" * 50)
        print("✅ Program completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Program interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()