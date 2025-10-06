# Design Document

## Overview

The unified main interpreter will consolidate all features from the existing SOUTK interpreter implementations (`soutk_enhanced.py`, `soutk_interpreter.py`, `soutk_ultimate.py`) into a single, comprehensive interpreter located at `src/soutk_interpreter.py`. This design creates a clean, maintainable codebase that serves as the definitive SOUTK interpreter while preserving all existing functionality and ensuring backward compatibility.

The interpreter will be implemented as a class-based system with clear separation of concerns, comprehensive error handling, and support for all SOUTK language features including data structures, functions, control flow, and interactive capabilities.

## Architecture

### Core Components

```
SoutkInterpreter (Main Class)
├── Core Execution Engine
│   ├── Line-by-line execution
│   ├── Expression evaluation
│   └── Error handling with line numbers
├── Variable Management
│   ├── Variable storage and retrieval
│   ├── Scope management for functions
│   └── Type handling (strings, numbers, booleans, arrays)
├── Function System
│   ├── Function definition parsing
│   ├── Parameter handling and validation
│   ├── Return value management
│   └── Local scope isolation
├── Data Structures
│   ├── Stack operations (forge, push, pop, peek)
│   ├── Queue operations (forge, enqueue, dequeue, front)
│   └── Linked List operations (forge, link, unlink, traverse)
├── Control Flow
│   ├── Conditional statements (if/else)
│   ├── Loop constructs (while, for)
│   └── Conditional expressions
└── I/O Operations
    ├── User input (listen command)
    ├── Output (speak command)
    └── String interpolation
```

### Data Structure Classes

The interpreter will include dedicated classes for each data structure:

- **SoutkStack**: LIFO operations with push, pop, peek, and show methods
- **SoutkQueue**: FIFO operations with enqueue, dequeue, front, and show methods  
- **SoutkLinkedList**: Dynamic list with link, unlink, insert_after, and traverse methods
- **SoutkNode**: Node class for linked list implementation

### Exception Handling

Custom exception classes for proper error management:

- **ReturnException**: Handles function return statements
- **SoutkError**: General SOUTK runtime errors with context

## Components and Interfaces

### Main Interpreter Class

```python
class SoutkInterpreter:
    def __init__(self):
        self.variables = {}           # Variable storage
        self.functions = {}           # Function definitions
        self.data_structures = {}     # Data structure instances
        self.line_number = 0          # Current line for error reporting
    
    # Core execution methods
    def execute(self, code)           # Main execution entry point
    def execute_line(self, line)      # Single line execution
    def eval_expr(self, expr)         # Expression evaluation
    
    # Variable management
    def set_variable(self, name, value)
    def get_variable(self, name)
    
    # Function management
    def define_function(self, name, params, body)
    def call_function(self, name, args)
    
    # Data structure operations
    def handle_data_structure_commands(self, line)
    
    # I/O operations
    def listen(self, prompt="")       # User input
    def speak(self, message)          # Output
    
    # Error handling
    def error(self, message)          # Error reporting with line numbers
```

### Expression Evaluation System

The expression evaluator will handle:

- **Arithmetic Operations**: +, -, *, /, %, **
- **String Operations**: Concatenation, interpolation
- **Logical Operations**: &&, ||, !, ==, !=, <, >, <=, >=
- **Array Operations**: Indexing, assignment, length
- **Variable Resolution**: Variable substitution in expressions
- **Function Calls**: Inline function execution
- **Type Coercion**: Automatic type conversion for operations

### Function System Interface

```python
# Function definition structure
{
    'name': 'function_name',
    'params': ['param1', 'param2'],
    'body': ['statement1', 'statement2', ...]
}

# Function call interface
def call_function(self, func_name, args_str):
    # Parse arguments
    # Validate parameter count
    # Create local scope
    # Execute function body
    # Handle return values
    # Restore original scope
```

### Data Structure Command Interface

All data structure commands follow a consistent pattern:

```
forge <type> <name>        # Create data structure
<operation> <name> [args]  # Perform operation on data structure
show<type> <name>          # Display data structure contents
```

## Data Models

### Variable Storage

Variables are stored in a dictionary with support for:

- **Strings**: Text values with quote handling
- **Numbers**: Integer and floating-point values
- **Booleans**: true/false values with proper string conversion
- **Arrays**: Lists with indexing and length operations
- **References**: Pointers to data structures

### Function Storage

Functions are stored as dictionaries containing:

```python
{
    'params': ['param1', 'param2'],  # Parameter names
    'body': ['line1', 'line2']       # Function body statements
}
```

### Data Structure Storage

Data structures are stored in a separate dictionary with instances of:

- **SoutkStack**: Stack instances with LIFO operations
- **SoutkQueue**: Queue instances with FIFO operations
- **SoutkLinkedList**: Linked list instances with dynamic operations

### Scope Management

Function calls create temporary scopes:

1. Save current variable state
2. Set function parameters as local variables
3. Execute function body
4. Capture return value
5. Restore original variable state
6. Return captured value

## Error Handling

### Error Reporting System

All errors include:

- **Line Number**: Current execution line for context
- **Error Type**: Specific error category
- **Error Message**: Clear description of the issue
- **Context**: Relevant variable or function information

### Error Categories

- **Syntax Errors**: Invalid SOUTK syntax
- **Runtime Errors**: Execution-time issues
- **Type Errors**: Invalid type operations
- **Reference Errors**: Undefined variables or functions
- **Index Errors**: Array bounds violations
- **Parameter Errors**: Function call mismatches

### Graceful Degradation

The interpreter handles errors gracefully:

- Continue execution after non-fatal errors
- Provide helpful error messages
- Maintain interpreter state consistency
- Handle user interrupts (Ctrl+C, EOF)

## Testing Strategy

### Unit Testing Approach

Test coverage will include:

1. **Core Functionality Tests**
   - Variable assignment and retrieval
   - Expression evaluation accuracy
   - Function definition and calling
   - Control flow execution

2. **Data Structure Tests**
   - Stack operations (push, pop, peek)
   - Queue operations (enqueue, dequeue, front)
   - Linked list operations (link, unlink, traverse)
   - Data structure creation and management

3. **Error Handling Tests**
   - Invalid syntax handling
   - Runtime error recovery
   - Function parameter validation
   - Array bounds checking

4. **Integration Tests**
   - Complete program execution
   - Feature interaction testing
   - Backward compatibility verification
   - Performance benchmarking

### Test Data Strategy

- **Positive Test Cases**: Valid SOUTK programs
- **Negative Test Cases**: Invalid syntax and runtime errors
- **Edge Cases**: Boundary conditions and unusual inputs
- **Regression Tests**: Existing program compatibility

### Validation Approach

- Compare outputs with existing interpreters
- Verify all example programs execute correctly
- Ensure all language features work as documented
- Test interactive features with simulated input

## Implementation Considerations

### Code Organization

The unified interpreter will be organized into logical sections:

1. **Imports and Constants**: Required modules and configuration
2. **Exception Classes**: Custom exception definitions
3. **Data Structure Classes**: Stack, Queue, LinkedList implementations
4. **Main Interpreter Class**: Core interpreter functionality
5. **Utility Functions**: Helper methods and utilities
6. **Entry Point**: Main execution function

### Performance Optimization

- Efficient expression evaluation with minimal regex usage
- Optimized variable lookup with dictionary access
- Streamlined function call overhead
- Memory-efficient data structure implementations

### Maintainability Features

- Comprehensive docstrings for all methods
- Clear variable and function naming
- Logical code organization and separation
- Extensive inline comments for complex logic

### Extensibility Design

The architecture supports future enhancements:

- Modular command handling for new features
- Pluggable data structure system
- Extensible expression evaluation
- Configurable error handling and reporting

This design ensures the unified main interpreter will be robust, maintainable, and fully compatible with existing SOUTK programs while providing a solid foundation for future language development.