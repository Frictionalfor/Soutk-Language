# Soutk Programming Language Reference

## Table of Contents
1. [Overview](#overview)
2. [Basic Syntax](#basic-syntax)
3. [Variables](#variables)
4. [Data Types](#data-types)
5. [Operators](#operators)
6. [Control Structures](#control-structures)
7. [Functions](#functions)
8. [Arrays](#arrays)
9. [Classes and Objects](#classes-and-objects)
10. [Data Structures](#data-structures)
11. [File I/O](#file-io)
12. [Error Handling](#error-handling)
13. [Built-in Functions](#built-in-functions)
14. [Comments](#comments)
15. [Examples](#examples)

---

## Overview

Soutk is a custom programming language with a unique magical syntax. It features functions, arrays, loops, conditionals, classes, file I/O, error handling, and more.

**File Extension:** `.stk`

---

## Basic Syntax

### Output Statement
```soutk
chant "Hello World";
chant variable_name;
chant "Value: " + variable_name;
```

### Statement Termination
- Statements can end with or without semicolons
- Semicolons are optional but recommended for clarity

---

## Variables

### Variable Declaration and Assignment
```soutk
// Direct assignment (no 'summon' needed)
x = 10;
name = "Alice";
flag = true;

// Multiple assignment
a, b, c = 1, 2, 3;

// Variable swapping
x, y = y, x;
```

### Variable Rules
- Variable names must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Case-sensitive
- No reserved keywords except language constructs

---

## Data Types

### Numbers
```soutk
integer = 42;
decimal = 3.14;
negative = -10;
```

### Strings
```soutk
text = "Hello World";
single_quotes = 'Also valid';
empty = "";

// Enhanced strings with methods
enhanced_text = enchant_string("Hello World");
length = enhanced_text.length();
upper = enhanced_text.upper();
```

### Booleans
```soutk
is_true = true;
is_false = false;
```

### Arrays
```soutk
numbers = [1, 2, 3, 4, 5];
names = ["Alice", "Bob", "Charlie"];
mixed = [1, "hello", true, 3.14];
nested = [[1, 2], [3, 4]];
empty_array = [];
```

---

## Operators

### Arithmetic Operators
```soutk
result = 10 + 5;    // Addition: 15
result = 10 - 5;    // Subtraction: 5
result = 10 * 5;    // Multiplication: 50
result = 10 / 5;    // Division: 2
```

### Comparison Operators
```soutk
x == y    // Equal to
x != y    // Not equal to
x < y     // Less than
x <= y    // Less than or equal to
x > y     // Greater than
x >= y    // Greater than or equal to
```

### Logical Operators
```soutk
condition1 && condition2    // AND
condition1 || condition2    // OR
not condition              // NOT
```

### String Concatenation
```soutk
greeting = "Hello " + name + "!";
message = "Count: " + number;
```

---

## Control Structures

### If-Else Statements

#### Block Syntax
```soutk
if condition {
    // statements
} else {
    // statements
}
```

#### Single Statement Syntax
```soutk
if condition:
    statement
```

### While Loops
```soutk
while condition {
    // statements
}
```

### For Loops
```soutk
for (initialization; condition; increment) {
    // statements
}
```

### Stride Loops (Custom Loop)
```soutk
stride variable from start_value to end_value {
    // statements
}
```

### Break and Continue
```soutk
stride i from 1 to 10 {
    if i == 3:
        continue;    // Skip iteration
    if i == 8:
        break;       // Exit loop
    chant "Number: " + i;
}
```

---

## Functions

### Function Definition
```soutk
spell function_name(parameter1, parameter2) {
    // function body
    return value;  // optional
}
```

### Function Call
```soutk
cast function_name(argument1, argument2);
```

### Examples
```soutk
spell greet(name) {
    chant "Hello, " + name + "!";
}

spell add(a, b) {
    return a + b;
}

cast greet("World");
result = cast add(5, 3);
```

---

## Arrays

### Array Creation and Access
```soutk
array_name = [element1, element2, element3];
first_element = array_name[0];
last_element = array_name[len(array_name) - 1];
```

### Nested Array Access
```soutk
matrix = [[1, 2], [3, 4]];
element = matrix[0][1];  // Gets 2
```

---

## Classes and Objects

### Class Definition
```soutk
enchant ClassName {
    spell construct(param1, param2) {
        this.property1 = param1;
        this.property2 = param2;
    }
    
    spell methodName(param) {
        // method body
        return value;
    }
}
```

### Object Creation and Usage
```soutk
object = conjure ClassName(arg1, arg2);
object.methodName(argument);
property_value = object.property1;
```

### Example
```soutk
enchant Person {
    spell construct(name, age) {
        this.name = name;
        this.age = age;
    }
    
    spell greet() {
        chant "Hello, I'm " + this.name;
    }
    
    spell birthday() {
        this.age = this.age + 1;
    }
}

person = conjure Person("Alice", 25);
person.greet();
person.birthday();
```

---

## Data Structures

### Stacks
```soutk
forge stack stackName;
push stackName "item";
pop stackName;
peek stackName;
showstack stackName;
isempty stackName;
```

### Queues
```soutk
forge queue queueName;
enqueue queueName "item";
dequeue queueName;
front queueName;
showqueue queueName;
isempty queueName;
```

### Linked Lists
```soutk
forge linklist listName;
link listName "item";
unlink listName "item";
insertafter listName "afterItem" "newItem";
traverse listName;
isempty listName;
```

### Dictionaries (Grimoires)
```soutk
forge grimoire dictName;
bind dictName["key"] = "value";
value = dictName["key"];
```

---

## File I/O

### Reading Files
```soutk
scroll "filename.txt" into variable_name;
```

### Writing Files
```soutk
inscribe "filename.txt" with data;
```

### Appending to Files
```soutk
append "filename.txt" with data;
```

---

## Error Handling

### Ward/Rescue Blocks
```soutk
ward {
    // risky code
    result = 10 / 0;
} rescue error {
    chant "Error occurred: " + error;
    // error handling code
}
```

---

## Built-in Functions

### Basic Functions
- `chant(value)` - Output/print
- `listen(prompt)` - Get user input
- `len(array)` - Array length
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float

### Math Functions
- `sqrt(number)` - Square root
- `sin(angle)` - Sine function
- `cos(angle)` - Cosine function
- `tan(angle)` - Tangent function
- `abs(number)` - Absolute value
- `round(number)` - Round to nearest integer
- `floor(number)` - Round down
- `ceil(number)` - Round up
- `pow(base, exponent)` - Power function
- `random(min, max)` - Random number

### String Methods
- `text.length()` - String length
- `text.upper()` - Convert to uppercase
- `text.lower()` - Convert to lowercase
- `text.split(delimiter)` - Split string
- `text.contains(substring)` - Check if contains substring
- `text.startswith(prefix)` - Check if starts with prefix
- `text.endswith(suffix)` - Check if ends with suffix

---

## Comments

### Single-line Comments
```soutk
// This is a single-line comment
chant "Hello";  // Comment at end of line
```

---

## Examples

### Complete Program Examples

#### Hello World
```soutk
chant "Hello, World!";
```

#### Interactive Program
```soutk
name = listen("What's your name? ");
age = int(listen("How old are you? "));

if age >= 18 {
    chant "Hello " + name + ", you are an adult!";
} else {
    chant "Hello " + name + ", you are young!";
}
```

#### Class Example
```soutk
enchant Calculator {
    spell construct() {
        this.result = 0;
    }
    
    spell add(a, b) {
        this.result = a + b;
        return this.result;
    }
    
    spell getResult() {
        return this.result;
    }
}

calc = conjure Calculator();
sum = calc.add(10, 5);
chant "Result: " + sum;
```

#### File Processing
```soutk
// Read data from file
scroll "input.txt" into data;
chant "File content: " + data;

// Process and save
processed = "Processed: " + data;
inscribe "output.txt" with processed;
```

#### Error Handling Example
```soutk
ward {
    number = int(listen("Enter a number: "));
    result = 100 / number;
    chant "Result: " + result;
} rescue error {
    chant "Error: " + error;
    chant "Please enter a valid non-zero number.";
}
```

---

## Language Keywords

**Control Flow:** `if`, `else`, `while`, `for`, `stride`, `break`, `continue`, `return`

**Functions:** `spell`, `cast`

**Variables:** `summon` (optional)

**Classes:** `enchant`, `conjure`, `this`

**Data Structures:** `forge`, `push`, `pop`, `peek`, `enqueue`, `dequeue`, `front`, `link`, `unlink`, `traverse`, `bind`

**File I/O:** `scroll`, `inscribe`, `append`

**Error Handling:** `ward`, `rescue`

**I/O:** `chant`, `listen`

**Literals:** `true`, `false`

---

*This reference covers all current features of the Soutk programming language. For more examples, see the examples/ directory.*