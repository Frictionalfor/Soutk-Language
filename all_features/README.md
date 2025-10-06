# 🧙‍♂️ Soutk Programming Language - Complete Guide & Feature Showcase

Welcome to the **complete guide** for the Soutk programming language! This directory contains comprehensive examples, syntax references, and tutorials for every feature of Soutk.

## � Qeuick Start

**Run your first Soutk program:**
```bash
python soutk.py all_features/01_basic_output_variables.stk
```

**Test all features at once:**
```bash
python soutk.py all_features/13_complete_feature_test.stk
```

---

## 📖 Complete Soutk Syntax Reference

### 🔰 **Basic Syntax**

#### **Comments**
```soutk
// Single line comment
/* Multi-line
   comment */
```

#### **Variables (summon)**
```soutk
summon name = "Alice";           // String
summon age = 25;                 // Number
summon is_student = true;        // Boolean
summon grades = [85, 92, 78];    // Array
```

#### **Output (chant)**
```soutk
chant "Hello, World!";           // Print text
chant name;                      // Print variable
chant "Age: " + age;             // Print with concatenation
```

#### **User Input (listen)**
```soutk
summon user_name = listen("Enter your name: ");
summon user_age = listen("Enter your age: ");
```

### 🔢 **Data Types**

#### **Numbers**
```soutk
summon integer = 42;
summon decimal = 3.14159;
summon negative = -17;
```

#### **Strings**
```soutk
summon greeting = "Hello";
summon name = 'World';
summon message = greeting + " " + name;  // Concatenation
summon first_char = message[0];          // Character access
summon length = len(message);            // String length
```

#### **Booleans**
```soutk
summon is_true = true;
summon is_false = false;
summon result = not is_false;            // true
```

#### **Arrays**
```soutk
summon numbers = [1, 2, 3, 4, 5];
summon mixed = [42, "hello", true];
summon first = numbers[0];               // Access element
summon size = len(numbers);              // Array length
numbers[1] = 99;                         // Modify element
```

### ➕ **Operators**

#### **Arithmetic Operators**
```soutk
summon a = 10;
summon b = 3;

summon addition = a + b;        // 13
summon subtraction = a - b;     // 7
summon multiplication = a * b;  // 30
summon division = a / b;        // 3.333...
summon modulus = a % b;         // 1 (remainder)
```

#### **Comparison Operators**
```soutk
summon x = 10;
summon y = 20;

summon equal = x == y;          // false
summon not_equal = x != y;      // true
summon less_than = x < y;       // true
summon greater_than = x > y;    // false
summon less_equal = x <= y;     // true
summon greater_equal = x >= y;  // false
```

#### **Logical Operators**
```soutk
summon a = true;
summon b = false;

summon and_result = a && b;     // false
summon or_result = a || b;      // true
summon not_result = not a;      // false
```

### 🎛️ **Control Structures**

#### **If-Else Statements**
```soutk
summon score = 85;

if score >= 90:
{
    chant "Grade: A";
}
else:
{
    if score >= 80:
    {
        chant "Grade: B";
    }
    else:
    {
        if score >= 70:
        {
            chant "Grade: C";
        }
        else:
        {
            chant "Grade: F";
        }
    }
}
```

#### **Loops (stride)**
```soutk
// Basic for loop
stride i from 1 to 5:
{
    chant "Count: " + i;
}

// Loop with array
summon fruits = ["apple", "banana", "orange"];
stride j from 0 to len(fruits) - 1:
{
    chant "Fruit " + (j + 1) + ": " + fruits[j];
}

// Nested loops
stride row from 1 to 3:
{
    stride col from 1 to 3:
    {
        chant "(" + row + "," + col + ")";
    }
}
```

### ⚡ **Functions (spell/cast)**

#### **Function Definition**
```soutk
spell greet(name):
{
    chant "Hello, " + name + "!";
}

spell add(a, b):
{
    return a + b;
}

spell factorial(n):
{
    if n <= 1:
    {
        return 1;
    }
    return n * cast factorial(n - 1);
}
```

#### **Function Calling**
```soutk
cast greet("Alice");                    // Call void function
summon result = cast add(5, 3);         // Call function with return
summon fact5 = cast factorial(5);       // Recursive function call
```

#### **Advanced Functions**
```soutk
// Function with multiple parameters
spell calculate_grade(name, scores):
{
    summon total = 0;
    stride i from 0 to len(scores) - 1:
    {
        total = total + scores[i];
    }
    summon average = total / len(scores);
    chant name + "'s average: " + average;
    return average;
}

// Higher-order function simulation
spell apply_to_array(arr, operation):
{
    summon result = [];
    stride i from 0 to len(arr) - 1:
    {
        if operation == "double":
        {
            result = result + [arr[i] * 2];
        }
        else:
        {
            if operation == "square":
            {
                result = result + [arr[i] * arr[i]];
            }
        }
    }
    return result;
}
```

### 🏗️ **Object-Oriented Programming**

#### **Class Definition**
```soutk
class Person:
{
    spell __init__(self, name, age):
    {
        self.name = name;
        self.age = age;
    }
    
    spell introduce(self):
    {
        chant "Hi, I'm " + self.name + ", age " + self.age;
    }
    
    spell get_age_group(self):
    {
        if self.age < 18:
        {
            return "minor";
        }
        else:
        {
            return "adult";
        }
    }
}
```

#### **Object Creation and Usage**
```soutk
summon person1 = new Person("Alice", 25);
person1.introduce();
summon age_group = person1.get_age_group();
chant "Age group: " + age_group;
```

#### **Inheritance**
```soutk
class Student extends Person:
{
    spell __init__(self, name, age, school):
    {
        super.__init__(self, name, age);
        self.school = school;
        self.grades = [];
    }
    
    spell add_grade(self, subject, grade):
    {
        self.grades = self.grades + [[subject, grade]];
    }
    
    spell introduce(self):
    {
        chant "Hi, I'm " + self.name + ", I study at " + self.school;
    }
}

summon student = new Student("Bob", 20, "Soutk University");
student.introduce();
student.add_grade("Math", 95);
```

### 🛡️ **Error Handling**

#### **Try-Catch Blocks**
```soutk
try:
{
    summon result = 10 / 0;  // This will cause an error
    chant "Result: " + result;
}
catch error:
{
    chant "Error caught: " + error;
    chant "Division by zero handled!";
}
```

#### **Throwing Errors**
```soutk
spell divide_safe(a, b):
{
    if b == 0:
    {
        throw "Cannot divide by zero!";
    }
    return a / b;
}

try:
{
    summon result = cast divide_safe(10, 0);
}
catch error:
{
    chant "Custom error: " + error;
}
```

#### **Nested Error Handling**
```soutk
spell complex_operation(data, index):
{
    try:
    {
        if index >= len(data):
        {
            throw "Index out of bounds";
        }
        
        try:
        {
            summon value = data[index];
            return value * 2;
        }
        catch inner_error:
        {
            throw "Inner operation failed: " + inner_error;
        }
    }
    catch outer_error:
    {
        chant "Outer error: " + outer_error;
        return -1;
    }
}
```

### 🛠️ **Built-in Functions**

```soutk
// Length function
summon text = "Hello";
summon arr = [1, 2, 3, 4];
chant len(text);        // 5
chant len(arr);         // 4

// Type checking
summon num = 42;
summon str = "hello";
chant typeof(num);      // "number"
chant typeof(str);      // "string"

// String conversion
summon number = 123;
summon text = str(number);  // "123"
chant "Number as string: " + text;
```

---

## 📁 **Feature Files Overview**

| File | Level | Features Demonstrated |
|------|-------|----------------------|
| `01_basic_output_variables.stk` | 🔰 Beginner | Variables (`summon`), output (`chant`), basic data types |
| `02_arithmetic_operations.stk` | 🔰 Beginner | Math operations (`+`, `-`, `*`, `/`, `%`), operator precedence |
| `03_string_operations.stk` | 🔰 Beginner | String manipulation, concatenation, character access |
| `04_arrays.stk` | 🔰 Beginner | Array creation, indexing, `len()` function |
| `05_comparison_operators.stk` | 🎯 Intermediate | Comparison logic (`==`, `!=`, `<`, `>`, `<=`, `>=`) |
| `06_logical_operators.stk` | 🎯 Intermediate | Boolean operations (`&&`, `||`, `not`) |
| `07_control_structures.stk` | 🎯 Intermediate | If-else statements, nested conditions |
| `08_loops.stk` | 🎯 Intermediate | For loops (`stride`), nested loops |
| `09_functions.stk` | 🎯 Intermediate | Function definition (`spell`), calling (`cast`), return values |
| `10_user_input.stk` | 🎯 Intermediate | Interactive input with `listen` command |
| `11_built_in_functions.stk` | 🎯 Intermediate | Built-in functions (`len()`, `str()`, `typeof()`) |
| `12_advanced_features.stk` | 🚀 Advanced | Complex nested structures, advanced algorithms |
| `13_complete_feature_test.stk` | 🧪 Testing | Comprehensive test of all 14 major features |
| `14_object_oriented.stk` | 🚀 Advanced | Classes, objects, inheritance (`extends`), polymorphism |
| `15_error_handling.stk` | 🚀 Advanced | Try-catch blocks, error throwing, nested error handling |
| `16_modern_features.stk` | 🌟 Expert | Latest features, functional programming, advanced patterns |

---

## 🎓 **Complete Learning Path**

### **Phase 1: Fundamentals** (Files 01-04) 
**Time: 1-2 hours**

Start here if you're new to programming or Soutk:

1. **Variables & Output** (`01_basic_output_variables.stk`)
   - Learn `summon` for variables
   - Learn `chant` for output
   - Understand data types

2. **Math Operations** (`02_arithmetic_operations.stk`)
   - Arithmetic operators
   - Operator precedence
   - Mathematical expressions

3. **Text Handling** (`03_string_operations.stk`)
   - String creation and manipulation
   - String concatenation
   - Character access

4. **Lists & Arrays** (`04_arrays.stk`)
   - Array creation and indexing
   - Array operations
   - Length function

### **Phase 2: Logic & Control** (Files 05-08)
**Time: 2-3 hours**

Build logical thinking and program flow:

5. **Comparisons** (`05_comparison_operators.stk`)
   - Equality and inequality
   - Greater/less than comparisons
   - Boolean results

6. **Boolean Logic** (`06_logical_operators.stk`)
   - AND, OR, NOT operations
   - Complex logical expressions
   - Truth tables

7. **Decision Making** (`07_control_structures.stk`)
   - If-else statements
   - Nested conditions
   - Complex decision trees

8. **Repetition** (`08_loops.stk`)
   - For loops with `stride`
   - Nested loops
   - Loop patterns

### **Phase 3: Functions & Interaction** (Files 09-11)
**Time: 2-3 hours**

Learn to organize code and interact with users:

9. **Code Organization** (`09_functions.stk`)
   - Function definition with `spell`
   - Function calling with `cast`
   - Parameters and return values

10. **User Interaction** (`10_user_input.stk`)
    - Getting input with `listen`
    - Interactive programs
    - Input validation

11. **Built-in Tools** (`11_built_in_functions.stk`)
    - Length function `len()`
    - Type checking `typeof()`
    - String conversion `str()`

### **Phase 4: Advanced Concepts** (Files 12, 14-16)
**Time: 3-4 hours**

Master advanced programming concepts:

12. **Complex Logic** (`12_advanced_features.stk`)
    - Nested data structures
    - Complex algorithms
    - Advanced problem solving

14. **Object-Oriented Programming** (`14_object_oriented.stk`)
    - Classes and objects
    - Inheritance with `extends`
    - Method overriding

15. **Error Management** (`15_error_handling.stk`)
    - Try-catch blocks
    - Error throwing
    - Graceful error handling

16. **Modern Features** (`16_modern_features.stk`)
    - Functional programming concepts
    - Advanced patterns
    - Performance considerations

### **Phase 5: Validation** (File 13)
**Time: 30 minutes**

13. **Complete Testing** (`13_complete_feature_test.stk`)
    - Runs 14 comprehensive tests
    - Validates all features work
    - Confirms language mastery

---

## 🎯 **How to Use This Guide**

### **For Complete Beginners:**
1. Start with Phase 1 files (01-04)
2. Practice each concept before moving on
3. Run each file and understand the output
4. Modify examples to experiment

### **For Experienced Programmers:**
1. Skim through Phase 1-2 for syntax
2. Focus on Phase 3-4 for Soutk-specific features
3. Run the comprehensive test (file 13)
4. Explore advanced features (files 14-16)

### **For Educators:**
1. Use files 01-11 for structured lessons
2. File 13 for assessment
3. Files 14-16 for advanced students
4. Each file is self-contained and teachable

### **For Contributors:**
1. Run file 13 to verify all features work
2. Use files as regression tests
3. Add new features following the same pattern
4. Update tests when adding new capabilities

---

## 🧪 **Testing & Validation**

### **Quick Test:**
```bash
python soutk.py all_features/13_complete_feature_test.stk
```

### **Individual Feature Tests:**
```bash
# Test basic features
python soutk.py all_features/01_basic_output_variables.stk

# Test advanced features
python soutk.py all_features/14_object_oriented.stk

# Test error handling
python soutk.py all_features/15_error_handling.stk
```

### **Expected Results:**
- All tests should pass ✅
- No error messages (except in error handling demos)
- Clear, readable output
- Comprehensive feature validation

---

## 🌟 **Advanced Usage Examples**

### **Complex Program Structure:**
```soutk
// Multi-class system with error handling
class Calculator:
{
    spell __init__(self):
    {
        self.history = [];
    }
    
    spell calculate(self, operation, a, b):
    {
        try:
        {
            summon result = 0;
            if operation == "add":
            {
                result = a + b;
            }
            else:
            {
                if operation == "divide":
                {
                    if b == 0:
                    {
                        throw "Division by zero!";
                    }
                    result = a / b;
                }
            }
            
            self.history = self.history + [[operation, a, b, result]];
            return result;
        }
        catch error:
        {
            chant "Calculation error: " + error;
            return null;
        }
    }
}
```

### **Functional Programming Style:**
```soutk
spell map_array(arr, operation):
{
    summon result = [];
    stride i from 0 to len(arr) - 1:
    {
        if operation == "square":
        {
            result = result + [arr[i] * arr[i]];
        }
        else:
        {
            if operation == "double":
            {
                result = result + [arr[i] * 2];
            }
        }
    }
    return result;
}

summon numbers = [1, 2, 3, 4, 5];
summon squared = cast map_array(numbers, "square");
summon doubled = cast map_array(numbers, "double");
```

---

## 🏆 **Mastery Checklist**

After completing all files, you should be able to:

### **Basic Programming** ✅
- [ ] Create and use variables
- [ ] Perform arithmetic operations
- [ ] Handle strings and arrays
- [ ] Use comparison and logical operators

### **Control Flow** ✅
- [ ] Write if-else statements
- [ ] Create loops with proper syntax
- [ ] Nest control structures
- [ ] Handle complex conditions

### **Functions** ✅
- [ ] Define functions with parameters
- [ ] Return values from functions
- [ ] Call functions properly
- [ ] Understand scope and recursion

### **Object-Oriented Programming** ✅
- [ ] Create classes with methods
- [ ] Use inheritance effectively
- [ ] Understand polymorphism
- [ ] Design object hierarchies

### **Error Handling** ✅
- [ ] Use try-catch blocks
- [ ] Throw custom errors
- [ ] Handle nested errors
- [ ] Write robust code

### **Advanced Concepts** ✅
- [ ] Work with complex data structures
- [ ] Apply functional programming concepts
- [ ] Optimize for performance
- [ ] Use modern language features

---

## 🎉 **Congratulations!**

Once you've completed all files and passed the comprehensive test, you're officially a **Soutk Programming Wizard!** 🧙‍♂️✨

You now have the skills to:
- Build complete applications in Soutk
- Teach others the Soutk language
- Contribute to the Soutk project
- Create your own programming projects

**Welcome to the Soutk community!** 🚀

---

## 📞 **Need Help?**

- 📖 Check the main documentation in `/docs/`
- 🎯 Run the comprehensive test for validation
- 🔍 Look at specific feature files for examples
- 💡 Experiment with the code examples

**Happy coding with Soutk!** 🌟