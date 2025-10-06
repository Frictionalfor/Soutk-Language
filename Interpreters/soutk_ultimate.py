"""
Ultimate Soutk Interpreter - Complete Programming Language
Features: File I/O, Error Handling, Dictionaries, String Methods, Classes, Modules, Advanced Loops, Math Library
"""

import re
import os
import json
import math
import random
import importlib.util
from pathlib import Path

class ReturnException(Exception):
    """Custom exception for handling return statements"""
    def __init__(self, value):
        self.value = value
        super().__init__(f"RETURN:{value}")

class SoutkError(Exception):
    """Custom exception for Soutk error handling"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class SoutkStack:
    """Stack data structure for Soutk"""
    def __init__(self, name):
        self.name = name
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.items:
            return self.items.pop()
        return None
    
    def peek(self):
        if self.items:
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def show(self):
        return list(reversed(self.items))

class SoutkQueue:
    """Queue data structure for Soutk"""
    def __init__(self, name):
        self.name = name
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.items:
            return self.items.pop(0)
        return None
    
    def front(self):
        if self.items:
            return self.items[0]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def show(self):
        return self.items.copy()

class SoutkNode:
    """Node for linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None

class SoutkLinkedList:
    """Linked List data structure for Soutk"""
    def __init__(self, name):
        self.name = name
        self.head = None
    
    def link(self, data):
        new_node = SoutkNode(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def unlink(self, data):
        if not self.head:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        return False
    
    def insert_after(self, after_data, new_data):
        current = self.head
        while current:
            if current.data == after_data:
                new_node = SoutkNode(new_data)
                new_node.next = current.next
                current.next = new_node
                return True
            current = current.next
        return False
    
    def traverse(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def is_empty(self):
        return self.head is None

class SoutkGrimoire:
    """Dictionary/Map data structure for Soutk"""
    def __init__(self, name):
        self.name = name
        self.data = {}
    
    def bind(self, key, value):
        self.data[key] = value
    
    def unbind(self, key):
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def lookup(self, key):
        return self.data.get(key, None)
    
    def keys(self):
        return list(self.data.keys())
    
    def values(self):
        return list(self.data.values())
    
    def is_empty(self):
        return len(self.data) == 0
    
    def show(self):
        return dict(self.data)

class SoutkString:
    """Enhanced string with methods"""
    def __init__(self, value):
        self.value = str(value)
    
    def length(self):
        return len(self.value)
    
    def upper(self):
        return SoutkString(self.value.upper())
    
    def lower(self):
        return SoutkString(self.value.lower())
    
    def split(self, delimiter=" "):
        return [SoutkString(part) for part in self.value.split(delimiter)]
    
    def replace(self, old, new):
        return SoutkString(self.value.replace(old, new))
    
    def contains(self, substring):
        return substring in self.value
    
    def startswith(self, prefix):
        return self.value.startswith(prefix)
    
    def endswith(self, suffix):
        return self.value.endswith(suffix)
    
    def strip(self):
        return SoutkString(self.value.strip())
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'"{self.value}"'

class SoutkClass:
    """Class definition for Soutk"""
    def __init__(self, name, methods, constructor=None):
        self.name = name
        self.methods = methods
        self.constructor = constructor

class SoutkObject:
    """Object instance for Soutk"""
    def __init__(self, class_def, interpreter):
        self.class_def = class_def
        self.interpreter = interpreter
        self.attributes = {}
    
    def get_attribute(self, name):
        return self.attributes.get(name, None)
    
    def set_attribute(self, name, value):
        self.attributes[name] = value
    
    def call_method(self, method_name, args):
        if method_name in self.class_def.methods:
            method = self.class_def.methods[method_name]
            # Create temporary scope with 'this' reference
            old_variables = self.interpreter.variables.copy()
            self.interpreter.variables['this'] = self
            
            try:
                # Set parameters
                for param, arg in zip(method['params'], args):
                    self.interpreter.variables[param] = arg
                
                # Execute method body
                result = None
                try:
                    self.interpreter.execute(method['body'])
                except ReturnException as ret:
                    result = ret.value
                
                return result
            finally:
                # Restore original variables
                self.interpreter.variables = old_variables
        else:
            raise ValueError(f"Method '{method_name}' not found in class '{self.class_def.name}'")

class SoutkInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.data_structures = {}
        self.classes = {}
        self.modules = {}
        self.line_number = 0
        self.current_file = None
        
        # Initialize math functions
        self.init_math_functions()
    
    def init_math_functions(self):
        """Initialize built-in math functions"""
        self.math_functions = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'abs': abs,
            'round': round,
            'floor': math.floor,
            'ceil': math.ceil,
            'pow': pow,
            'log': math.log,
            'random': lambda a=0, b=1: random.uniform(a, b) if isinstance(a, float) or isinstance(b, float) else random.randint(a, b)
        }
    
    def listen(self, prompt=""):
        """Get input from user"""
        try:
            if prompt:
                if isinstance(prompt, str) and prompt.startswith('"') and prompt.endswith('"'):
                    prompt = prompt[1:-1]
                user_input = input(prompt)
            else:
                user_input = input()
            
            return user_input.strip()
        except KeyboardInterrupt:
            return ""
        except EOFError:
            return ""
    
    def error(self, message):
        """Display error with line number"""
        print(f"❌ Line {self.line_number}: {message}")
    
    def handle_file_operations(self, line):
        """Handle file I/O operations"""
        line = line.rstrip(';')
        
        # SCROLL - Read file
        scroll_match = re.match(r'scroll\s+"([^"]+)"\s+into\s+(\w+)', line)
        if scroll_match:
            filename = scroll_match.group(1)
            var_name = scroll_match.group(2)
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.variables[var_name] = content
                print(f"📜 Scrolled '{filename}' into '{var_name}'")
            except FileNotFoundError:
                self.error(f"File '{filename}' not found")
            except Exception as e:
                self.error(f"Error reading file '{filename}': {str(e)}")
            return True
        
        # INSCRIBE - Write file
        inscribe_match = re.match(r'inscribe\s+"([^"]+)"\s+with\s+(.+)', line)
        if inscribe_match:
            filename = inscribe_match.group(1)
            data_expr = inscribe_match.group(2)
            
            try:
                data = self.eval_expr(data_expr)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(str(data))
                print(f"📝 Inscribed data into '{filename}'")
            except Exception as e:
                self.error(f"Error writing to file '{filename}': {str(e)}")
            return True
        
        # APPEND - Append to file
        append_match = re.match(r'append\s+"([^"]+)"\s+with\s+(.+)', line)
        if append_match:
            filename = append_match.group(1)
            data_expr = append_match.group(2)
            
            try:
                data = self.eval_expr(data_expr)
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(str(data) + '\n')
                print(f"📝 Appended data to '{filename}'")
            except Exception as e:
                self.error(f"Error appending to file '{filename}': {str(e)}")
            return True
        
        return False
    
    def handle_module_operations(self, line):
        """Handle module import operations"""
        line = line.rstrip(';')
        
        # INVOKE - Import module
        invoke_match = re.match(r'invoke\s+"([^"]+)"(?:\s+as\s+(\w+))?', line)
        if invoke_match:
            filename = invoke_match.group(1)
            alias = invoke_match.group(2)
            
            try:
                # Read and execute the module
                with open(filename, 'r', encoding='utf-8') as f:
                    module_code = f.read()
                
                # Create a new interpreter instance for the module
                module_interpreter = SoutkInterpreter()
                module_interpreter.current_file = filename
                module_interpreter.execute(module_code)
                
                # Import functions and variables
                module_name = alias if alias else Path(filename).stem
                self.modules[module_name] = {
                    'functions': module_interpreter.functions.copy(),
                    'variables': module_interpreter.variables.copy(),
                    'classes': module_interpreter.classes.copy()
                }
                
                print(f"🔮 Invoked module '{filename}' as '{module_name}'")
            except FileNotFoundError:
                self.error(f"Module '{filename}' not found")
            except Exception as e:
                self.error(f"Error importing module '{filename}': {str(e)}")
            return True
        
        return False
    
    def handle_class_operations(self, lines, i):
        """Handle class definitions"""
        line = lines[i]
        
        # ENCHANT - Class definition
        enchant_match = re.match(r'enchant\s+(\w+)\s*[:{]', line)
        if enchant_match:
            class_name = enchant_match.group(1)
            
            # Parse class body
            class_body, end_i = self.parse_class_body(lines, i)
            
            # Extract methods and constructor
            methods = {}
            constructor = None
            
            j = 0
            while j < len(class_body):
                body_line = class_body[j].strip()
                
                if body_line.startswith("spell construct"):
                    # Constructor
                    construct_match = re.search(r'spell\s+construct\s*\((.*?)\):', body_line)
                    if construct_match:
                        params_str = construct_match.group(1).strip()
                        params = [param.strip() for param in params_str.split(',')] if params_str else []
                        
                        # Parse constructor body
                        method_body, method_end = self.parse_method_body(class_body, j)
                        constructor = {
                            'params': params,
                            'body': method_body
                        }
                        j = method_end
                        continue
                
                elif body_line.startswith("spell "):
                    # Regular method
                    spell_match = re.search(r'spell\s+(\w+)\s*\((.*?)\):', body_line)
                    if spell_match:
                        method_name = spell_match.group(1)
                        params_str = spell_match.group(2).strip()
                        params = [param.strip() for param in params_str.split(',')] if params_str else []
                        
                        # Parse method body
                        method_body, method_end = self.parse_method_body(class_body, j)
                        methods[method_name] = {
                            'params': params,
                            'body': method_body
                        }
                        j = method_end
                        continue
                
                j += 1
            
            # Store class definition
            self.classes[class_name] = SoutkClass(class_name, methods, constructor)
            print(f"✨ Enchanted class '{class_name}'")
            
            return end_i
        
        return i + 1
    
    def parse_class_body(self, lines, start):
        """Parse class body and return statements"""
        body = []
        i = start
        depth = 0
        
        # Find opening brace
        while i < len(lines):
            if '{' in lines[i]:
                depth = 1
                i += 1
                break
            i += 1
        
        # Collect body statements
        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if '{' in line:
                depth += 1
            if '}' in line:
                depth -= 1
            
            if depth > 0:
                body.append(line)
            i += 1
        
        return body, i
    
    def parse_method_body(self, class_body, start):
        """Parse method body within class"""
        body = []
        i = start
        depth = 0
        
        # Find opening brace
        while i < len(class_body):
            if '{' in class_body[i]:
                depth = 1
                i += 1
                break
            i += 1
        
        # Collect method statements
        while i < len(class_body) and depth > 0:
            line = class_body[i].strip()
            if '{' in line:
                depth += 1
            if '}' in line:
                depth -= 1
            
            if depth > 0:
                body.append(line)
            i += 1
        
        return body, i
    
    def handle_error_handling(self, lines, i):
        """Handle ward/rescue error handling"""
        line = lines[i]
        
        if line.strip().startswith("ward"):
            # Parse ward block
            ward_body, ward_end = self.parse_function_body(lines, i)
            
            # Check for rescue block
            rescue_body = []
            error_var = "error"
            
            if ward_end < len(lines) and lines[ward_end].strip().startswith("rescue"):
                rescue_line = lines[ward_end].strip()
                rescue_match = re.match(r'rescue\s+(\w+)\s*:', rescue_line)
                if rescue_match:
                    error_var = rescue_match.group(1)
                else:
                    # Default rescue without variable
                    error_var = "error"
                
                rescue_body, rescue_end = self.parse_function_body(lines, ward_end)
                ward_end = rescue_end
            
            # Execute ward block with error handling
            try:
                self.execute(ward_body)
            except Exception as e:
                if rescue_body:
                    # Set error variable and execute rescue block
                    old_error = self.variables.get(error_var)
                    # Convert exception to string, handling different error types
                    error_message = str(e)
                    if "Invalid expression:" in error_message:
                        error_message = "Expression evaluation error"
                    elif "division by zero" in error_message.lower():
                        error_message = "Division by zero error"
                    
                    self.variables[error_var] = error_message
                    try:
                        self.execute(rescue_body)
                    finally:
                        if old_error is not None:
                            self.variables[error_var] = old_error
                        elif error_var in self.variables:
                            del self.variables[error_var]
                else:
                    # Re-raise if no rescue block
                    raise e
            
            return ward_end
        
        return i + 1
    
    def eval_expr(self, expr):
        """Evaluate expressions safely with all enhancements"""
        expr = expr.strip()
        
        # Handle string literals
        string_literals = []
        def replace_strings(match):
            string_literals.append(match.group(0))
            return f"__STRING_{len(string_literals)-1}__"
        
        expr = re.sub(r'"[^"]*"', replace_strings, expr)
        expr = re.sub(r"'[^']*'", replace_strings, expr)
        
        # Handle object attribute access: obj.attribute (but not method calls or decimal numbers)
        attribute_access_pattern = r'([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)(?!\()'
        def replace_attribute_access(match):
            obj_name = match.group(1)
            attr_name = match.group(2)
            
            # Skip if this looks like a decimal number (e.g., 1.5708)
            if obj_name.isdigit():
                return match.group(0)
            
            if obj_name in self.variables:
                obj = self.variables[obj_name]
                if isinstance(obj, SoutkObject):
                    attr_value = obj.get_attribute(attr_name)
                    if attr_value is not None:
                        if isinstance(attr_value, str):
                            return f'"{attr_value}"'
                        else:
                            return str(attr_value)
                    else:
                        return f"UNDEFINED_ATTR_{attr_name}"
                # Don't process SoutkString attributes here - let method calls handle them
                elif isinstance(obj, SoutkString):
                    return match.group(0)  # Return unchanged for method processing
            
            return f"ATTR_ERROR_{obj_name}.{attr_name}"
        
        # Only apply attribute access for non-method calls
        temp_expr = re.sub(attribute_access_pattern, replace_attribute_access, expr)
        if "METHOD_ERROR" not in temp_expr:
            expr = temp_expr
        
        # Handle object method calls: obj.method(args)
        method_call_pattern = r'(\w+)\.(\w+)\((.*?)\)'
        def replace_method_calls(match):
            obj_name = match.group(1)
            method_name = match.group(2)
            args_str = match.group(3)
            
            if obj_name in self.variables:
                obj = self.variables[obj_name]
                
                # Handle SoutkString methods
                if isinstance(obj, SoutkString):
                    if hasattr(obj, method_name):
                        method = getattr(obj, method_name)
                        if args_str.strip():
                            # Restore string literals in arguments before processing
                            restored_args_str = args_str
                            for i, literal in enumerate(string_literals):
                                restored_args_str = restored_args_str.replace(f"__STRING_{i}__", literal)
                            
                            args = []
                            for arg in restored_args_str.split(','):
                                arg = arg.strip()
                                if arg.startswith('"') and arg.endswith('"'):
                                    args.append(arg[1:-1])  # Remove quotes
                                elif arg.startswith("'") and arg.endswith("'"):
                                    args.append(arg[1:-1])  # Remove quotes
                                else:
                                    args.append(self.eval_expr(arg))
                            
                            result = method(*args)
                        else:
                            result = method()
                        
                        if isinstance(result, SoutkString):
                            return f'"{result.value}"'
                        elif isinstance(result, list):
                            return str([str(item) for item in result])
                        elif isinstance(result, bool):
                            return "true" if result else "false"
                        else:
                            return str(result)
                
                # Handle SoutkObject methods
                elif isinstance(obj, SoutkObject):
                    if args_str.strip():
                        args = [self.eval_expr(arg.strip()) for arg in args_str.split(',')]
                    else:
                        args = []
                    
                    result = obj.call_method(method_name, args)
                    return str(result) if result is not None else "None"
                
                # Handle Grimoire methods
                elif isinstance(obj, SoutkGrimoire):
                    if method_name == "lookup":
                        key = self.eval_expr(args_str)
                        result = obj.lookup(key)
                        return f'"{result}"' if isinstance(result, str) else str(result)
                    elif method_name == "keys":
                        return str(obj.keys())
                    elif method_name == "values":
                        return str(obj.values())
            
            return f"METHOD_ERROR_{obj_name}.{method_name}"
        
        expr = re.sub(method_call_pattern, replace_method_calls, expr)
        
        # Handle array access
        array_access_pattern = r'(\w+)\[([^\]]+)\]'
        def replace_array_access(match):
            array_name = match.group(1)
            index_expr = match.group(2)
            
            if array_name in self.variables:
                array = self.variables[array_name]
            elif array_name in self.data_structures:
                array = self.data_structures[array_name]
                if isinstance(array, list):
                    try:
                        if index_expr.isdigit():
                            index = int(index_expr)
                        elif index_expr in self.variables:
                            index = self.variables[index_expr]
                        else:
                            safe_dict = {"__builtins__": {}}
                            safe_dict.update(self.variables)
                            index = eval(index_expr, safe_dict)
                        
                        if isinstance(index, int) and 0 <= index < len(array):
                            result = array[index]
                            if isinstance(result, str):
                                return f'"{result}"'
                            else:
                                return str(result)
                        else:
                            return f"INDEX_ERROR_{index}"
                    except:
                        return f"EVAL_ERROR_{index_expr}"
                elif isinstance(array, SoutkGrimoire):
                    # Dictionary access - restore string literal if needed
                    key = index_expr
                    if key.startswith('__STRING_') and key.endswith('__'):
                        # Find the original string literal
                        string_index = int(key.replace('__STRING_', '').replace('__', ''))
                        if string_index < len(string_literals):
                            key = string_literals[string_index].strip('"\'')
                    else:
                        key = key.strip('"\'')
                    
                    result = array.lookup(key)
                    if result is not None:
                        if isinstance(result, str):
                            return f'"{result}"'
                        else:
                            return str(result)
                    else:
                        return "None"
                else:
                    return f"NOT_ARRAY_{array_name}"
            else:
                return f"UNDEFINED_{array_name}"
        
        expr = re.sub(array_access_pattern, replace_array_access, expr)
        
        # Replace variables with their values
        for var_name, var_value in self.variables.items():
            pattern = rf'\b{re.escape(var_name)}\b'
            if re.search(pattern, expr):
                if isinstance(var_value, str):
                    replacement = f'"{var_value}"'
                elif isinstance(var_value, bool):
                    if '+' in expr and ('"' in expr or "'" in expr):
                        replacement = f'"{"true" if var_value else "false"}"'
                    else:
                        replacement = "True" if var_value else "False"
                elif isinstance(var_value, (list, SoutkGrimoire)):
                    replacement = str(var_value)
                elif isinstance(var_value, SoutkString):
                    replacement = f'"{var_value.value}"'
                else:
                    replacement = str(var_value)
                expr = re.sub(pattern, replacement, expr)
        
        # Restore string literals
        for i, literal in enumerate(string_literals):
            expr = expr.replace(f"__STRING_{i}__", literal)
        
        # Handle string concatenation
        if '+' in expr and not any(op in expr for op in ['==', '!=', '<=', '>=', '<', '>']):
            has_strings = '"' in expr or "'" in expr
            
            if not has_strings:
                for var_name, var_value in self.variables.items():
                    if var_name in expr and isinstance(var_value, bool):
                        has_strings = True
                        break
            
            if has_strings:
                parts = []
                current_part = ""
                in_quotes = False
                quote_char = None
                paren_depth = 0
                
                for char in expr:
                    if char in ['"', "'"] and not in_quotes:
                        in_quotes = True
                        quote_char = char
                        current_part += char
                    elif char == quote_char and in_quotes:
                        in_quotes = False
                        current_part += char
                    elif char == '(' and not in_quotes:
                        paren_depth += 1
                        current_part += char
                    elif char == ')' and not in_quotes:
                        paren_depth -= 1
                        current_part += char
                    elif char == '+' and not in_quotes and paren_depth == 0:
                        if current_part.strip():
                            parts.append(current_part.strip())
                        current_part = ""
                    else:
                        current_part += char
                
                if current_part.strip():
                    parts.append(current_part.strip())
                
                result = ""
                for part in parts:
                    if part.startswith('"') and part.endswith('"'):
                        result += part[1:-1]
                    elif part.startswith("'") and part.endswith("'"):
                        result += part[1:-1]
                    elif part in self.variables:
                        var_value = self.variables[part]
                        if isinstance(var_value, bool):
                            result += "true" if var_value else "false"
                        else:
                            result += str(var_value)
                    else:
                        try:
                            safe_dict = {
                                "__builtins__": {"len": len, "str": str, "int": int, "float": float, "listen": self.listen},
                                "true": True,
                                "false": False
                            }
                            safe_dict.update(self.variables)
                            safe_dict.update(self.math_functions)
                            evaluated_val = eval(part, safe_dict)
                            if isinstance(evaluated_val, bool):
                                result += "true" if evaluated_val else "false"
                            else:
                                result += str(evaluated_val)
                        except:
                            result += str(part)
                return result
        
        # Handle logical operators
        expr = expr.replace("&&", " and ").replace("||", " or ")
        
        try:
            # Handle invoke function calls in expressions
            invoke_pattern = r'invoke\s+(\w+)\s*\((.*?)\)'
            def replace_invoke(match):
                func_name = match.group(1)
                args_str = match.group(2)
                try:
                    result = self.call_function(func_name, args_str)
                    return str(result)
                except Exception as e:
                    return f"ERROR_{str(e)}"
            
            expr = re.sub(invoke_pattern, replace_invoke, expr)
            
            # Handle cast function calls in expressions (for backward compatibility)
            cast_pattern = r'cast\s+(\w+)\s*\((.*?)\)'
            def replace_cast(match):
                func_name = match.group(1)
                args_str = match.group(2)
                try:
                    result = self.call_function(func_name, args_str)
                    return str(result)
                except Exception as e:
                    return f"ERROR_{str(e)}"
            
            expr = re.sub(cast_pattern, replace_cast, expr)
            
            # Add variables to the evaluation context
            safe_dict = {
                "__builtins__": {"len": len, "str": str, "int": int, "float": float, "not": lambda x: not x, "listen": self.listen},
                "true": True,
                "false": False,
                "True": True,
                "False": False
            }
            safe_dict.update(self.variables)
            safe_dict.update(self.math_functions)
            result = eval(expr, safe_dict)
            
            if '+' in expr and ('"' in expr or "'" in expr):
                if isinstance(result, bool):
                    return "true" if result else "false"
            
            return result
        except Exception as e:
            if "can only concatenate str" in str(e) and "bool" in str(e):
                fixed_expr = expr
                for var_name, var_value in self.variables.items():
                    if isinstance(var_value, bool):
                        bool_str = "true" if var_value else "false"
                        fixed_expr = fixed_expr.replace(str(var_value), f'"{bool_str}"')
                
                try:
                    safe_dict = {
                        "__builtins__": {"len": len, "str": str, "int": int, "float": float, "not": lambda x: not x, "listen": self.listen},
                        "true": True,
                        "false": False,
                        "True": True,
                        "False": False
                    }
                    safe_dict.update(self.variables)
                    safe_dict.update(self.math_functions)
                    return eval(fixed_expr, safe_dict)
                except:
                    pass
            
            raise ValueError(f"Invalid expression: {expr} - {str(e)}")
    
    def call_function(self, func_name, args_str):
        """Call a function and return its result"""
        if func_name not in self.functions:
            raise ValueError(f"Function '{func_name}' not defined")
        
        func = self.functions[func_name]
        
        # Parse arguments
        args = []
        if args_str:
            current_arg = ""
            in_quotes = False
            quote_char = None
            
            for char in args_str:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_arg += char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    current_arg += char
                elif char == ',' and not in_quotes:
                    if current_arg.strip():
                        args.append(current_arg.strip())
                    current_arg = ""
                else:
                    current_arg += char
            
            if current_arg.strip():
                args.append(current_arg.strip())
        
        if len(args) != len(func['params']):
            raise ValueError(f"Function '{func_name}' expects {len(func['params'])} arguments, got {len(args)}")
        
        old_variables = self.variables.copy()
        return_value = None
        
        try:
            for param, arg in zip(func['params'], args):
                self.variables[param] = self.eval_expr(arg)
            
            try:
                self.execute(func['body'])
            except ReturnException as ret:
                return_value = ret.value
            except Exception as e:
                if str(e).startswith("RETURN:"):
                    return_value_str = str(e)[7:]
                    if return_value_str:
                        try:
                            return_value = eval(return_value_str)
                        except:
                            return_value = return_value_str
                    else:
                        return_value = None
                else:
                    raise e
        finally:
            self.variables = old_variables
        
        return return_value if return_value is not None else 0
    
    def handle_data_structure_commands(self, line):
        """Handle data structure commands"""
        line = line.rstrip(';')
        parts = line.split()
        
        if len(parts) < 2:
            return False
        
        command = parts[0]
        
        # FORGE commands - create data structures
        if command == "forge":
            if len(parts) < 3:
                self.error("forge command requires type and name")
                return True
            
            ds_type = parts[1]
            ds_name = parts[2]
            
            if ds_type == "stack":
                self.data_structures[ds_name] = SoutkStack(ds_name)
                print(f"⚔️ Forged stack '{ds_name}'")
            elif ds_type == "queue":
                self.data_structures[ds_name] = SoutkQueue(ds_name)
                print(f"📋 Forged queue '{ds_name}'")
            elif ds_type == "linklist":
                self.data_structures[ds_name] = SoutkLinkedList(ds_name)
                print(f"🔗 Forged linked list '{ds_name}'")
            elif ds_type == "grimoire":
                self.data_structures[ds_name] = SoutkGrimoire(ds_name)
                print(f"📚 Forged grimoire '{ds_name}'")
            else:
                self.error(f"Unknown data structure type: {ds_type}")
            
            return True
        
        # BIND - Dictionary assignment
        elif command == "bind":
            if len(parts) < 2:
                return False
            
            # Parse: bind dict["key"] = value
            bind_match = re.match(r'bind\s+(\w+)\[([^\]]+)\]\s*=\s*(.+)', line)
            if bind_match:
                dict_name = bind_match.group(1)
                key_expr = bind_match.group(2)
                value_expr = bind_match.group(3)
                
                if dict_name in self.data_structures:
                    ds = self.data_structures[dict_name]
                    if isinstance(ds, SoutkGrimoire):
                        key = self.eval_expr(key_expr)
                        value = self.eval_expr(value_expr)
                        ds.bind(key, value)
                        print(f"📖 Bound '{key}' = '{value}' in grimoire '{dict_name}'")
                    else:
                        self.error(f"'{dict_name}' is not a grimoire")
                else:
                    self.error(f"Grimoire '{dict_name}' not found")
                return True
        
        # Stack, Queue, LinkedList commands (keeping existing implementation)
        elif command in ["push", "pop", "peek", "showstack", "enqueue", "dequeue", "front", "showqueue", 
                        "link", "unlink", "insertafter", "traverse", "isempty"]:
            return self.handle_existing_ds_commands(line, command, parts)
        
        return False
    
    def handle_existing_ds_commands(self, line, command, parts):
        """Handle existing data structure commands"""
        # STACK commands
        if command == "push":
            if len(parts) < 3:
                self.error("push command requires stack name and value")
                return True
            
            stack_name = parts[1]
            value = " ".join(parts[2:])
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                value = self.eval_expr(value)
            
            if stack_name in self.data_structures:
                ds = self.data_structures[stack_name]
                if isinstance(ds, SoutkStack):
                    ds.push(value)
                    print(f"⬆️ Pushed '{value}' to stack '{stack_name}'")
                else:
                    self.error(f"'{stack_name}' is not a stack")
            else:
                self.error(f"Stack '{stack_name}' not found")
            return True
        
        elif command == "pop":
            if len(parts) < 2:
                self.error("pop command requires stack name")
                return True
            
            stack_name = parts[1]
            if stack_name in self.data_structures:
                ds = self.data_structures[stack_name]
                if isinstance(ds, SoutkStack):
                    value = ds.pop()
                    if value is not None:
                        print(f"⬇️ Popped '{value}' from stack '{stack_name}'")
                    else:
                        print(f"Stack '{stack_name}' is empty")
                else:
                    self.error(f"'{stack_name}' is not a stack")
            else:
                self.error(f"Stack '{stack_name}' not found")
            return True
        
        elif command == "peek":
            if len(parts) < 2:
                self.error("peek command requires stack name")
                return True
            
            stack_name = parts[1]
            if stack_name in self.data_structures:
                ds = self.data_structures[stack_name]
                if isinstance(ds, SoutkStack):
                    value = ds.peek()
                    if value is not None:
                        print(f"👁️ Top of stack '{stack_name}': '{value}'")
                    else:
                        print(f"Stack '{stack_name}' is empty")
                else:
                    self.error(f"'{stack_name}' is not a stack")
            else:
                self.error(f"Stack '{stack_name}' not found")
            return True
        
        elif command == "showstack":
            if len(parts) < 2:
                self.error("showstack command requires stack name")
                return True
            
            stack_name = parts[1]
            if stack_name in self.data_structures:
                ds = self.data_structures[stack_name]
                if isinstance(ds, SoutkStack):
                    items = ds.show()
                    print(f"📚 Stack '{stack_name}': {items}")
                else:
                    self.error(f"'{stack_name}' is not a stack")
            else:
                self.error(f"Stack '{stack_name}' not found")
            return True
        
        # QUEUE commands
        elif command == "enqueue":
            if len(parts) < 3:
                self.error("enqueue command requires queue name and value")
                return True
            
            queue_name = parts[1]
            value = " ".join(parts[2:])
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                value = self.eval_expr(value)
            
            if queue_name in self.data_structures:
                ds = self.data_structures[queue_name]
                if isinstance(ds, SoutkQueue):
                    ds.enqueue(value)
                    print(f"➡️ Enqueued '{value}' to queue '{queue_name}'")
                else:
                    self.error(f"'{queue_name}' is not a queue")
            else:
                self.error(f"Queue '{queue_name}' not found")
            return True
        
        elif command == "dequeue":
            if len(parts) < 2:
                self.error("dequeue command requires queue name")
                return True
            
            queue_name = parts[1]
            if queue_name in self.data_structures:
                ds = self.data_structures[queue_name]
                if isinstance(ds, SoutkQueue):
                    value = ds.dequeue()
                    if value is not None:
                        print(f"⬅️ Dequeued '{value}' from queue '{queue_name}'")
                    else:
                        print(f"Queue '{queue_name}' is empty")
                else:
                    self.error(f"'{queue_name}' is not a queue")
            else:
                self.error(f"Queue '{queue_name}' not found")
            return True
        
        elif command == "front":
            if len(parts) < 2:
                self.error("front command requires queue name")
                return True
            
            queue_name = parts[1]
            if queue_name in self.data_structures:
                ds = self.data_structures[queue_name]
                if isinstance(ds, SoutkQueue):
                    value = ds.front()
                    if value is not None:
                        print(f"👁️ Front of queue '{queue_name}': '{value}'")
                    else:
                        print(f"Queue '{queue_name}' is empty")
                else:
                    self.error(f"'{queue_name}' is not a queue")
            else:
                self.error(f"Queue '{queue_name}' not found")
            return True
        
        elif command == "showqueue":
            if len(parts) < 2:
                self.error("showqueue command requires queue name")
                return True
            
            queue_name = parts[1]
            if queue_name in self.data_structures:
                ds = self.data_structures[queue_name]
                if isinstance(ds, SoutkQueue):
                    items = ds.show()
                    print(f"📋 Queue '{queue_name}': {items}")
                else:
                    self.error(f"'{queue_name}' is not a queue")
            else:
                self.error(f"Queue '{queue_name}' not found")
            return True
        
        # LINKED LIST commands
        elif command == "link":
            if len(parts) < 3:
                self.error("link command requires list name and value")
                return True
            
            list_name = parts[1]
            value = " ".join(parts[2:])
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                value = self.eval_expr(value)
            
            if list_name in self.data_structures:
                ds = self.data_structures[list_name]
                if isinstance(ds, SoutkLinkedList):
                    ds.link(value)
                    print(f"🔗 Linked '{value}' to list '{list_name}'")
                else:
                    self.error(f"'{list_name}' is not a linked list")
            else:
                self.error(f"Linked list '{list_name}' not found")
            return True
        
        elif command == "unlink":
            if len(parts) < 3:
                self.error("unlink command requires list name and value")
                return True
            
            list_name = parts[1]
            value = " ".join(parts[2:])
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                value = self.eval_expr(value)
            
            if list_name in self.data_structures:
                ds = self.data_structures[list_name]
                if isinstance(ds, SoutkLinkedList):
                    if ds.unlink(value):
                        print(f"⛓️‍💥 Unlinked '{value}' from list '{list_name}'")
                    else:
                        print(f"Value '{value}' not found in list '{list_name}'")
                else:
                    self.error(f"'{list_name}' is not a linked list")
            else:
                self.error(f"Linked list '{list_name}' not found")
            return True
        
        elif command == "insertafter":
            if len(parts) < 4:
                self.error("insertafter command requires list name, after value, and new value")
                return True
            
            list_name = parts[1]
            after_value = parts[2]
            if after_value.startswith('"') and after_value.endswith('"'):
                after_value = after_value[1:-1]
            elif after_value.startswith("'") and after_value.endswith("'"):
                after_value = after_value[1:-1]
            else:
                after_value = self.eval_expr(after_value)
            
            new_value = " ".join(parts[3:])
            if new_value.startswith('"') and new_value.endswith('"'):
                new_value = new_value[1:-1]
            elif new_value.startswith("'") and new_value.endswith("'"):
                new_value = new_value[1:-1]
            else:
                new_value = self.eval_expr(new_value)
            
            if list_name in self.data_structures:
                ds = self.data_structures[list_name]
                if isinstance(ds, SoutkLinkedList):
                    if ds.insert_after(after_value, new_value):
                        print(f"🔗 Inserted '{new_value}' after '{after_value}' in list '{list_name}'")
                    else:
                        print(f"Value '{after_value}' not found in list '{list_name}'")
                else:
                    self.error(f"'{list_name}' is not a linked list")
            else:
                self.error(f"Linked list '{list_name}' not found")
            return True
        
        elif command == "traverse":
            if len(parts) < 2:
                self.error("traverse command requires list name")
                return True
            
            list_name = parts[1]
            if list_name in self.data_structures:
                ds = self.data_structures[list_name]
                if isinstance(ds, SoutkLinkedList):
                    items = ds.traverse()
                    print(f"🔗 List '{list_name}': {' -> '.join(map(str, items))}")
                else:
                    self.error(f"'{list_name}' is not a linked list")
            else:
                self.error(f"Linked list '{list_name}' not found")
            return True
        
        elif command == "isempty":
            if len(parts) < 2:
                self.error("isempty command requires data structure name")
                return True
            
            ds_name = parts[1]
            if ds_name in self.data_structures:
                ds = self.data_structures[ds_name]
                is_empty = ds.is_empty()
                print(f"📊 '{ds_name}' is {'empty' if is_empty else 'not empty'}")
            else:
                self.error(f"Data structure '{ds_name}' not found")
            return True
        
        return False
    
    def find_function_end(self, lines, start):
        """Find the end of a function definition"""
        i = start
        depth = 0
        
        while i < len(lines):
            if '{' in lines[i]:
                depth = 1
                i += 1
                break
            i += 1
        
        while i < len(lines) and depth > 0:
            line = lines[i]
            if '{' in line:
                depth += 1
            if '}' in line:
                depth -= 1
            i += 1
        
        return i
    
    def parse_function_body(self, lines, start):
        """Parse function body and return the statements"""
        body = []
        i = start
        depth = 0
        
        while i < len(lines):
            if '{' in lines[i]:
                depth = 1
                i += 1
                break
            i += 1
        
        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if '{' in line:
                depth += 1
            if '}' in line:
                depth -= 1
            
            if depth > 0:
                body.append(line)
            i += 1
        
        return body
    
    def execute(self, code):
        """Execute Soutk code with all enhancements"""
        if isinstance(code, str):
            lines = [line.strip() for line in code.splitlines() 
                    if line.strip() and not line.strip().startswith('//')]
        else:
            lines = code
        
        i = 0
        while i < len(lines):
            self.line_number = i + 1
            line = lines[i].strip()
            
            try:
                # Check for file operations
                if self.handle_file_operations(line):
                    i += 1
                    continue
                
                # Check for module operations
                if self.handle_module_operations(line):
                    i += 1
                    continue
                
                # Check for error handling
                if line.startswith("ward"):
                    i = self.handle_error_handling(lines, i)
                    continue
                
                # Check for class definitions
                if line.startswith("enchant") and ("{" in line or ":" in line):
                    i = self.handle_class_operations(lines, i)
                    continue
                
                # FORGE SPELL - Function definitions (check before data structures)
                if line.startswith("forge spell"):
                    spell_match = re.search(r'forge spell\s+(\w+)\s*\((.*?)\)', line)
                    if spell_match:
                        func_name = spell_match.group(1)
                        params_str = spell_match.group(2).strip()
                        params = [param.strip() for param in params_str.split(',')] if params_str else []
                        
                        body = self.parse_function_body(lines, i)
                        
                        self.functions[func_name] = {
                            'params': params,
                            'body': body
                        }
                        
                        i = self.find_function_end(lines, i)
                        continue
                
                # Check for data structure commands (after function definitions)
                if self.handle_data_structure_commands(line):
                    i += 1
                    continue
                
                # CONJURE - Object creation
                if "conjure" in line:
                    conjure_match = re.match(r'(\w+)\s*=\s*conjure\s+(\w+)\s*\((.*?)\)', line)
                    if conjure_match:
                        var_name = conjure_match.group(1)
                        class_name = conjure_match.group(2)
                        args_str = conjure_match.group(3)
                        
                        if class_name in self.classes:
                            class_def = self.classes[class_name]
                            obj = SoutkObject(class_def, self)
                            
                            # Call constructor if exists
                            if class_def.constructor:
                                if args_str.strip():
                                    args = [self.eval_expr(arg.strip()) for arg in args_str.split(',')]
                                else:
                                    args = []
                                
                                # Execute constructor
                                old_variables = self.variables.copy()
                                self.variables['this'] = obj
                                
                                try:
                                    for param, arg in zip(class_def.constructor['params'], args):
                                        self.variables[param] = arg
                                    
                                    self.execute(class_def.constructor['body'])
                                except ReturnException:
                                    pass  # Constructors don't return values
                                finally:
                                    self.variables = old_variables
                            
                            self.variables[var_name] = obj
                            print(f"✨ Conjured {class_name} object '{var_name}'")
                        else:
                            self.error(f"Class '{class_name}' not defined")
                        
                        i += 1
                        continue
                
                # Enhanced string creation
                if "enchant_string" in line:
                    string_match = re.match(r'(\w+)\s*=\s*enchant_string\s*\((.+?)\)', line)
                    if string_match:
                        var_name = string_match.group(1)
                        value_expr = string_match.group(2)
                        value = self.eval_expr(value_expr)
                        self.variables[var_name] = SoutkString(value)
                        i += 1
                        continue
                
                # Handle SOUTK magical keywords
                
                elif line.startswith("chant"):
                    if line.startswith("chant "):
                        to_print = line[6:].strip(" ;")
                    elif line.startswith("chant("):
                        to_print = line[5:].strip(" ;")
                    else:
                        to_print = line[5:].strip(" ;")
                    
                    result = self.eval_expr(to_print)
                    if isinstance(result, str) and result.startswith('"') and result.endswith('"'):
                        result = result[1:-1]
                    print(result)
                
                elif line.startswith("return"):
                    if line == "return" or line == "return;":
                        raise ReturnException(None)
                    else:
                        return_expr = line[6:].strip(" ;")
                        return_value = self.eval_expr(return_expr)
                        raise ReturnException(return_value)
                
                # TRANSFORM - Variable assignment
                elif line.startswith("transform"):
                    transform_line = line[9:].strip()  # Remove "transform "
                    if '=' in transform_line:
                        var_name, expr = transform_line.split('=', 1)
                        var_name = var_name.strip()
                        expr = expr.strip(' ;')
                        
                        value = self.eval_expr(expr)
                        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        self.variables[var_name] = value
                    else:
                        self.error("Invalid transform syntax")
                
                # INVOKE - Function calls
                elif line.startswith("invoke"):
                    invoke_match = re.match(r'invoke\s+(\w+)\s*\((.*?)\)', line)
                    if invoke_match:
                        func_name = invoke_match.group(1)
                        args_str = invoke_match.group(2)
                        try:
                            result = self.call_function(func_name, args_str)
                            # Don't print the result unless it's assigned to a variable
                        except Exception as e:
                            self.error(str(e))
                    else:
                        self.error("Invalid invoke syntax")
                
                # LOOP - Enhanced loop support
                elif line.startswith("loop"):
                    loop_match = re.match(r'loop\s+(\w+)\s+from\s+(\d+|\w+)\s+to\s+(\d+|\w+)', line)
                    if loop_match:
                        var_name = loop_match.group(1)
                        start_val = loop_match.group(2)
                        end_val = loop_match.group(3)
                        
                        # Evaluate start and end values
                        start = self.eval_expr(start_val) if not start_val.isdigit() else int(start_val)
                        end = self.eval_expr(end_val) if not end_val.isdigit() else int(end_val)
                        
                        # Find loop body
                        loop_body = []
                        i += 1
                        depth = 0
                        
                        while i < len(lines):
                            body_line = lines[i].strip()
                            if '{' in body_line:
                                depth += 1
                            if '}' in body_line:
                                depth -= 1
                                if depth == 0:
                                    break
                            if depth > 0:
                                loop_body.append(body_line)
                            i += 1
                        
                        # Execute loop
                        old_var = self.variables.get(var_name)
                        try:
                            for loop_val in range(int(start), int(end) + 1):
                                self.variables[var_name] = loop_val
                                self.execute(loop_body)
                        finally:
                            if old_var is not None:
                                self.variables[var_name] = old_var
                            elif var_name in self.variables:
                                del self.variables[var_name]
                    else:
                        self.error("Invalid loop syntax")
                
                else:
                    # Variable assignment (with swapping support)
                    if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=', '<', '>']):
                        var_name, expr = line.split('=', 1)
                        var_name = var_name.strip()
                        expr = expr.strip(' ;')
                        
                        if ',' in var_name:
                            var_names = [v.strip() for v in var_name.split(',')]
                            if ',' in expr:
                                expr_parts = [e.strip() for e in expr.split(',')]
                                if len(var_names) == len(expr_parts):
                                    values = [self.eval_expr(e) for e in expr_parts]
                                    for var, val in zip(var_names, values):
                                        self.variables[var] = val
                                else:
                                    self.error(f"Mismatch in assignment: {len(var_names)} variables, {len(expr_parts)} values")
                            else:
                                self.error("Multiple variables require multiple values")
                        else:
                            # Check if this is object attribute assignment (obj.attr = value)
                            if '.' in var_name:
                                obj_name, attr_name = var_name.split('.', 1)
                                if obj_name in self.variables:
                                    obj = self.variables[obj_name]
                                    if isinstance(obj, SoutkObject):
                                        value = self.eval_expr(expr)
                                        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                                            value = value[1:-1]
                                        obj.set_attribute(attr_name, value)
                                    else:
                                        self.error(f"'{obj_name}' is not an object")
                                else:
                                    self.error(f"Object '{obj_name}' not found")
                            else:
                                # Regular variable assignment
                                value = self.eval_expr(expr)
                                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                                    value = value[1:-1]
                                self.variables[var_name] = value
            
            except StopIteration as ctrl:
                raise ctrl
            except ReturnException as ret:
                raise ret
            except Exception as e:
                self.error(str(e))
            
            i += 1

def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "hello.stk"
    
    try:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"❌ Error: File '{filename}' not found.")
            return
        
        with open(file_path, "r", encoding='utf-8') as f:
            code = f.read()
        
        print(f"🚀 Running Ultimate Soutk program: {filename}")
        print("=" * 50)
        
        interpreter = SoutkInterpreter()
        interpreter.current_file = filename
        interpreter.execute(code)
        
        print("=" * 50)
        print("✅ Program completed successfully!")
        
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")

if __name__ == "__main__":
    main()