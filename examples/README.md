# Soutk Programming Language Examples

This directory contains example programs demonstrating various features of the Soutk programming language.

## 📁 Example Categories

### **Basic Examples**
- `hello.stk` - Simple hello world program
- `variables_demo.stk` - Variable declaration and assignment
- `basic_math.stk` - Arithmetic operations
- `user_input.stk` - Interactive input with `listen()`

### **Control Structures**
- `conditionals.stk` - If/else statements
- `loops_demo.stk` - While, for, and stride loops
- `break_continue.stk` - Loop control statements

### **Functions**
- `simple_functions.stk` - Basic function definition and calling
- `function_parameters.stk` - Functions with parameters and return values
- `recursive_functions.stk` - Recursive function examples

### **Object-Oriented Programming**
- `basic_classes.stk` - Class definition and object creation
- `class_methods.stk` - Methods and properties
- `inheritance_demo.stk` - Class inheritance examples

### **Data Structures**
- `arrays_demo.stk` - Array creation and manipulation
- `stacks_demo.stk` - Stack operations
- `queues_demo.stk` - Queue operations
- `linked_lists_demo.stk` - Linked list operations
- `dictionaries_demo.stk` - Dictionary (grimoire) operations

### **Advanced Features**
- `file_operations.stk` - File reading, writing, and appending
- `error_handling.stk` - Ward/rescue error handling
- `string_methods.stk` - String manipulation methods
- `math_functions.stk` - Mathematical function examples

### **Complete Applications**
- `calculator.stk` - Interactive calculator
- `number_guessing_game.stk` - Guessing game with user input
- `text_processor.stk` - File processing application
- `inventory_system.stk` - Object-oriented inventory management
- `rpg_character.stk` - RPG character system

### **Test Programs**
- `comprehensive_test.stk` - Tests all language features
- `performance_test.stk` - Performance benchmarking
- `edge_cases.stk` - Edge case testing

## 🚀 Running Examples

To run any example:

```bash
python soutk.py examples/hello.stk
python soutk.py examples/calculator.stk
python soutk.py examples/rpg_character.stk
```

## 📚 Learning Path

**Beginners:**
1. Start with `hello.stk`
2. Try `variables_demo.stk`
3. Explore `conditionals.stk`
4. Learn functions with `simple_functions.stk`

**Intermediate:**
1. Object-oriented programming with `basic_classes.stk`
2. Data structures with `arrays_demo.stk`
3. File operations with `file_operations.stk`
4. Error handling with `error_handling.stk`

**Advanced:**
1. Complete applications like `calculator.stk`
2. Complex systems like `inventory_system.stk`
3. Game development with `rpg_character.stk`

## 🎯 Example Highlights

### Interactive Calculator
```soutk
// From calculator.stk
enchant Calculator {
    spell construct() {
        this.result = 0;
    }
    
    spell calculate(a, b, operation) {
        if operation == "+" {
            this.result = a + b;
        } else if operation == "-" {
            this.result = a - b;
        }
        return this.result;
    }
}
```

### File Processing
```soutk
// From file_operations.stk
scroll "input.txt" into data;
processed = "Processed: " + data.upper();
inscribe "output.txt" with processed;
```

### Error Handling
```soutk
// From error_handling.stk
ward {
    result = 10 / 0;
} rescue error {
    chant "Caught error: " + error;
}
```

---

*Each example is self-contained and includes comments explaining the concepts being demonstrated.*