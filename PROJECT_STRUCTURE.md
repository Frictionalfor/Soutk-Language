# Soutk Programming Language - Project Structure

## Directory Organization

```
Soutk-Language/
  soutk.py                     # Main entry point - run Soutk programs
  README.md                    # Project overview and quick start
  PROJECT_STRUCTURE.md         # This file - project organization
  LICENSE                      # MIT License

  src/                         # Source code modules
     soutk_interpreter.py     # Main interpreter implementation

  docs/                        # Documentation
     LANGUAGE_REFERENCE.md    # Complete language syntax reference
     CAPABILITIES.md          # Feature overview and examples

  examples/                    # Example programs and tutorials
     README.md                # Examples overview and learning path
     hello.stk                # Hello World program
     calculator.stk           # Interactive calculator
     rpg_character.stk        # RPG character system (OOP demo)
     data_structures_demo.stk # All data structures showcase
     advanced_demo.stk        # Advanced features demo
     [other examples...]      # Various feature demonstrations

  all_features/                # Complete feature showcase (16 files)
     README.md                # Feature showcase overview
     INDEX.md                 # Complete learning path and index
     01-16_*.stk              # All language features (16 files)

  tests/                       # Test suite
     run_all_tests.py         # Test runner script

  online_compiler/            # Browser-based compiler (HTML+JS+Python server)
     index.html               # Frontend web interface
     server.py                # Python backend for code execution
```

## Key Files Explained

### Main Entry Point
- **`soutk.py`** - The main script to run Soutk programs
  - Usage: `python soutk.py program.stk`
  - Handles command-line arguments
  - Provides help and version information

### Core Implementation
- **`src/soutk_interpreter.py`** - The complete interpreter
  - Contains all language features
  - Handles parsing and execution

### Documentation
- **`docs/LANGUAGE_REFERENCE.md`** - Complete syntax reference
- **`docs/CAPABILITIES.md`** - Feature overview and examples

### Examples
- **`examples/`** - Sample programs demonstrating language features
- **`all_features/`** - Comprehensive feature showcase with 16 individual files

### Tests
- **`tests/run_all_tests.py`** - Test runner script

### Online Compiler
- **`online_compiler/`** - Browser-based Soutk compiler and IDE
