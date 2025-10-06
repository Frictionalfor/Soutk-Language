"""
SOUTK Main Interpreter - Complete Programming Language with Magical Keywords
Supports: chant, transform, forge spell, invoke, loop, and all data structures
"""

import re
import os
import json
import math
import random
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

class SoutkInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.data_structures = {}
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
        
        # Handle array access
        array_access_pattern = r'(\w+)\[([^\]]+)\]'
        def replace_array_access(match):
            array_name = match.group(1)
            index_expr = match.group(2)
            
            if array_name in self.variables:
                array = self.variables[array_name]
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
                elif isinstance(var_value, list):
                    replacement = str(var_value)
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
        
        # Handle logical operators (be more careful with replacements)
        expr = re.sub(r'\band\b', ' and ', expr)
        expr = re.sub(r'\bor\b', ' or ', expr)
        
        try:
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
        
        # Check parameter count
        if len(args) != len(func['params']):
            raise ValueError(f"Function '{func_name}' expects {len(func['params'])} arguments, got {len(args)}")
        
        # Create temporary scope
        old_variables = self.variables.copy()
        return_value = None
        
        try:
            # Set parameters
            for param, arg in zip(func['params'], args):
                self.variables[param] = self.eval_expr(arg)
            
            # Execute function body and capture return value
            try:
                self.execute(func['body'])
            except ReturnException as ret:
                return_value = ret.value
        finally:
            # Restore original variables
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
            else:
                return False  # Not a data structure command
            
            return True
        
        # STACK commands
        elif command == "push":
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
        
        return False
    
    def find_function_end(self, lines, start):
        """Find the end of a function definition"""
        i = start
        depth = 0
        
        # Find opening brace
        while i < len(lines):
            if '{' in lines[i]:
                depth = 1
                i += 1
                break
            i += 1
        
        # Find closing brace
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
        
        return body
    
    def execute(self, code):
        """Execute Soutk code with magical keywords support"""
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
                # FORGE SPELL - Function definitions (check first)
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
                
                # Check for data structure commands
                if self.handle_data_structure_commands(line):
                    i += 1
                    continue
                
                # CHANT - Output
                if line.startswith("chant"):
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
                
                # IF statements
                elif line.startswith("if"):
                    if_match = re.match(r'if\s+(.+?)\s*\{?', line)
                    if if_match:
                        condition = if_match.group(1)
                        condition_result = self.eval_expr(condition)
                        
                        # Find if body
                        if_body = []
                        else_body = []
                        i += 1
                        depth = 0
                        in_else = False
                        
                        while i < len(lines):
                            body_line = lines[i].strip()
                            
                            if body_line.startswith("} else {") or body_line == "else {":
                                in_else = True
                                i += 1
                                continue
                            elif body_line.startswith("} else"):
                                in_else = True
                                # Handle inline else
                                else_content = body_line[6:].strip()
                                if else_content and not else_content.startswith("{"):
                                    else_body.append(else_content)
                                i += 1
                                continue
                            
                            if '{' in body_line:
                                depth += 1
                            if '}' in body_line:
                                depth -= 1
                                if depth == 0:
                                    break
                            
                            if depth > 0:
                                if in_else:
                                    else_body.append(body_line)
                                else:
                                    if_body.append(body_line)
                            i += 1
                        
                        # Execute appropriate body
                        if condition_result:
                            self.execute(if_body)
                        elif else_body:
                            self.execute(else_body)
                    else:
                        self.error("Invalid if syntax")
                
                # WHILE loops
                elif line.startswith("while"):
                    while_match = re.match(r'while\s+(.+?)\s*\{?', line)
                    if while_match:
                        condition = while_match.group(1)
                        
                        # Find while body
                        while_body = []
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
                                while_body.append(body_line)
                            i += 1
                        
                        # Execute while loop
                        while self.eval_expr(condition):
                            self.execute(while_body)
                    else:
                        self.error("Invalid while syntax")
                
                # RETURN statements
                elif line.startswith("return"):
                    if line == "return" or line == "return;":
                        raise ReturnException(None)
                    else:
                        return_expr = line[6:].strip(" ;")
                        return_value = self.eval_expr(return_expr)
                        raise ReturnException(return_value)
                
                # Regular variable assignment (fallback)
                elif '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=', '<', '>']):
                    var_name, expr = line.split('=', 1)
                    var_name = var_name.strip()
                    expr = expr.strip(' ;')
                    
                    value = self.eval_expr(expr)
                    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    self.variables[var_name] = value
            
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
        
        print(f"🧙‍♂️ Running SOUTK program: {filename}")
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