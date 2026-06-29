# Soutk Programming Language

**Version 1.0.0**

Soutk is a complete, multi-paradigm programming language with a distinctive magical theme. It supports procedural, object-oriented, and functional programming styles with a syntax designed to be both memorable and expressive.

## Features

- **Complete Programming Language** - Variables, functions, classes, loops, conditionals, modules
- **Multi-Paradigm** - Procedural, object-oriented, and functional programming support
- **Data Structures** - Stacks, queues, linked lists, dictionaries (grimoires)
- **File I/O** - Read, write, and append files
- **Error Handling** - ward/rescue blocks for robust error management
- **Object-Oriented** - Classes, objects, methods, constructors
- **Math Library** - Built-in mathematical functions (sqrt, sin, cos, tan, abs, round, floor, ceil, pow, log, random)
- **String Methods** - Advanced string manipulation (upper, lower, split, contains, length)
- **Variable Swapping** - Multiple assignment and swapping support
- **Interactive Input** - User input with listen() function

## Quick Start

### Installation

1. Clone this repository
2. Ensure you have Python 3.7+ installed
3. Run Soutk programs with: `python soutk.py your_program.stk`

### Hello World

```soutk
chant "Hello, World!";
```

### Variables and Functions

```soutk
// Variables
transform name = "Soutk Wizard";
transform level = 50;

// Functions
forge spell greet(person) {
    chant "Hello, " + person + "!";
}

invoke greet(name);
```

### Classes and Objects

```soutk
enchant Wizard {
    forge construct(name, power) {
        this.transform name = name;
        this.transform power = power;
    }
    
    forge spell castSpell(spellName) {
        chant this.name + " casts " + spellName + "!";
    }
}

transform gandalf = conjure Wizard("Gandalf", 100);
gandalf.castSpell("Fireball");
```

### Control Flow

```soutk
transform x = 10;

if x > 5 {
    chant "x is greater than 5";
} else {
    chant "x is not greater than 5";
}

loop i from 1 to 3 {
    chant "Iteration " + i;
}
```

## Documentation

- [Language Reference](docs/LANGUAGE_REFERENCE.md) - Complete syntax guide
- [Feature Overview](docs/CAPABILITIES.md) - All language capabilities
- [Examples](examples/) - Sample programs and tutorials

## Project Structure

```
Soutk-Language/
  soutk.py                 # Main interpreter
  README.md               # This file
  docs/                   # Documentation
  examples/               # Example programs
  tests/                  # Test suite
  src/                    # Source code modules
  online_compiler/        # Browser-based compiler
```

## Example Programs

- **Basic Examples** - Variables, functions, loops, conditionals
- **Data Structures** - Stacks, queues, linked lists, dictionaries
- **Object-Oriented** - Classes, objects, methods, constructors
- **File Operations** - Reading, writing, processing files
- **Mathematical** - Advanced calculations and algorithms
- **Games** - Text-based games and interactive programs
- **Utilities** - Practical programming examples

## Online Compiler

Run the browser-based compiler:

```bash
# Start server
python online_compiler/server.py

# Or specify port
python online_compiler/server.py --port 3000
```

Opens at `http://localhost:8080` with a full IDE (editor + output). Uses the real Soutk interpreter on the backend.

## Testing

```bash
# Run all examples
python soutk.py examples/hello.stk
python soutk.py examples/rpg_character.stk
python soutk.py examples/advanced_demo.stk

# Start online compiler
python online_compiler/server.py
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Why Soutk?

- **Educational** - Perfect for learning programming concepts
- **Memorable** - Magical syntax makes code easy to remember
- **Complete** - All features needed for real programming
- **Fun** - Coding feels like casting spells!
- **Powerful** - Can build real applications

## Language Philosophy

Soutk combines the power of modern programming languages with a magical theme that makes coding more engaging and memorable. Whether you're learning to program or building complex applications, Soutk provides all the tools you need with syntax that's both powerful and fun.

---

**Ready to start your magical coding journey?**

Check out the [examples](examples/) folder to see Soutk in action!
