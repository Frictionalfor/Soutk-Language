"""
Enhanced Soutk Interpreter - With Data Structures and Variable Swapping
"""

import re
from pathlib import Path

class ReturnException(Exception):
    """Custom exception for handling return statements"""
    def __init__(self, value):
        self.value = value
        super().__init__(f"RETURN:{value}")

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
        return list(reversed(self.items))  # Show top to bottom

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
        """Add node at the end"""
        new_node = SoutkNode(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def unlink(self, data):
        """Remove node by value"""
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
        """Insert node after specified node"""
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
        """Get all elements as list"""
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
        self.data_structures = {}  # Store stacks, queues, linked lists
        self.line_number = 0
    
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
            # Restore original variables
            self.variables = old_variables
        
        return return_value if return_value is not None else 0
    
    def error(self, message):
        """Display error with line number"""
        print(f"❌ Line {self.line_number}: {message}")
    
    def eval_expr(self, expr):
        """Evaluate expressions safely"""
        expr = expr.strip()
        
        # Handle string literals
        string_literals = []
        def replace_strings(match):
            string_literals.append(match.group(0))
            return f"__STRING_{len(string_literals)-1}__"
        
        expr = re.sub(r'"[^"]*"', replace_strings, expr)
        expr = re.sub(r"'[^']*'", replace_strings, expr)
        
        # Handle array access: array[index] - simplified to avoid infinite recursion
        array_access_pattern = r'(\w+)\[([^\]]+)\]'
        def replace_array_access(match):
            array_name = match.group(1)
            index_expr = match.group(2)
            
            if array_name in self.variables:
                array = self.variables[array_name]
                if isinstance(array, list):
                    try:
                        # Simple index evaluation - avoid recursion
                        if index_expr.isdigit():
                            index = int(index_expr)
                        elif index_expr in self.variables:
                            index = self.variables[index_expr]
                        else:
                            # For complex expressions, use eval carefully
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
        
        # Apply array access replacement
        expr = re.sub(array_access_pattern, replace_array_access, expr)
        
        # Replace variables with their values
        for var_name, var_value in self.variables.items():
            pattern = rf'\b{re.escape(var_name)}\b'
            if re.search(pattern, expr):
                if isinstance(var_value, str):
                    replacement = f'"{var_value}"'
                elif isinstance(var_value, bool):
                    # For string concatenation, convert booleans to string representation
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
        
        # Handle string concatenation - if there are any string literals, treat as concatenation
        if '+' in expr and not any(op in expr for op in ['==', '!=', '<=', '>=', '<', '>']):
            has_strings = '"' in expr or "'" in expr
            
            # Also check if any variables in the expression are booleans
            if not has_strings:
                for var_name, var_value in self.variables.items():
                    if var_name in expr and isinstance(var_value, bool):
                        has_strings = True
                        break
            
            if has_strings:
                # Split by + but be careful with nested expressions
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
                            # Try to evaluate as expression
                            safe_dict = {
                                "__builtins__": {"len": len, "str": str, "int": int, "float": float, "listen": self.listen},
                                "true": True,
                                "false": False
                            }
                            safe_dict.update(self.variables)
                            evaluated_val = eval(part, safe_dict)
                            # Convert all types to string properly
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
            # Handle cast function calls in expressions
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
            result = eval(expr, safe_dict)
            
            # Only convert booleans to strings if this is for string concatenation
            # Check if the expression contains string concatenation
            if '+' in expr and ('"' in expr or "'" in expr):
                if isinstance(result, bool):
                    return "true" if result else "false"
            
            return result
        except Exception as e:
            # If it's a concatenation error with boolean, try to fix it
            if "can only concatenate str" in str(e) and "bool" in str(e):
                # Try to fix boolean concatenation by converting booleans to strings
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
                    return eval(fixed_expr, safe_dict)
                except:
                    pass
            
            raise ValueError(f"Invalid expression: {expr} - {str(e)}")
    
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
    
    def handle_data_structure_commands(self, line):
        """Handle data structure commands"""
        # Remove semicolon if present
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
                self.error(f"Unknown data structure type: {ds_type}")
            
            return True
        
        # STACK commands
        elif command == "push":
            if len(parts) < 3:
                self.error("push command requires stack name and value")
                return True
            
            stack_name = parts[1]
            value = " ".join(parts[2:])  # Handle multi-word values
            # Remove quotes if present
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
            # Remove quotes if present
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
            # Remove quotes if present
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
            # Remove quotes if present
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
    
    def execute(self, code):
        """Execute Soutk code"""
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
                # Check for data structure commands first
                if self.handle_data_structure_commands(line):
                    i += 1
                    continue
                
                if line.startswith("spell"):
                    # Handle function definition
                    spell_match = re.search(r'spell\s+(\w+)\s*\((.*?)\):', line)
                    if spell_match:
                        func_name = spell_match.group(1)
                        params_str = spell_match.group(2).strip()
                        params = [param.strip() for param in params_str.split(',')] if params_str else []
                        
                        # Parse function body
                        body = self.parse_function_body(lines, i)
                        
                        # Store function
                        self.functions[func_name] = {
                            'params': params,
                            'body': body
                        }
                        
                        # Skip to end of function
                        i = self.find_function_end(lines, i)
                        continue
                
                elif line.startswith("cast "):
                    # Handle function call
                    cast_match = re.search(r'cast\s+(\w+)\s*\((.*?)\)', line)
                    if cast_match:
                        func_name = cast_match.group(1)
                        args_str = cast_match.group(2).strip()
                        
                        if func_name in self.functions:
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
                                self.error(f"Function '{func_name}' expects {len(func['params'])} arguments, got {len(args)}")
                            else:
                                # Create temporary scope
                                old_variables = self.variables.copy()
                                
                                # Set parameters
                                for param, arg in zip(func['params'], args):
                                    self.variables[param] = self.eval_expr(arg)
                                
                                # Execute function body
                                try:
                                    self.execute(func['body'])
                                except ReturnException as ret:
                                    pass  # Function returned, continue
                                except Exception as e:
                                    self.error(f"Error in function '{func_name}': {str(e)}")
                                finally:
                                    # Restore original variables
                                    self.variables = old_variables
                        else:
                            self.error(f"Function '{func_name}' not defined")
                
                elif line.startswith("chant"):
                    # Handle output
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
                
                elif line.startswith("summon "):
                    # Handle variable declaration (keeping for backward compatibility)
                    var_part = line[7:].strip()
                    
                    if '=' in var_part:
                        var_name, expr = var_part.split("=", 1)
                        expr = expr.strip(" ;")
                        
                        # Handle array creation
                        if expr.startswith('[') and expr.endswith(']'):
                            try:
                                # Use eval for array parsing to handle nested arrays
                                safe_dict = {
                                    "__builtins__": {"len": len, "str": str, "int": int, "float": float, "listen": self.listen},
                                    "true": True,
                                    "false": False
                                }
                                safe_dict.update(self.variables)
                                array_value = eval(expr, safe_dict)
                                self.variables[var_name.strip()] = array_value
                            except:
                                # Fallback to manual parsing
                                array_content = expr[1:-1].strip()
                                if array_content:
                                    elements = []
                                    current_element = ""
                                    in_quotes = False
                                    quote_char = None
                                    bracket_depth = 0
                                    
                                    for char in array_content:
                                        if char in ['"', "'"] and not in_quotes:
                                            in_quotes = True
                                            quote_char = char
                                            current_element += char
                                        elif char == quote_char and in_quotes:
                                            in_quotes = False
                                            current_element += char
                                        elif char == '[' and not in_quotes:
                                            bracket_depth += 1
                                            current_element += char
                                        elif char == ']' and not in_quotes:
                                            bracket_depth -= 1
                                            current_element += char
                                        elif char == ',' and not in_quotes and bracket_depth == 0:
                                            if current_element.strip():
                                                elements.append(self.eval_expr(current_element.strip()))
                                            current_element = ""
                                        else:
                                            current_element += char
                                    
                                    if current_element.strip():
                                        elements.append(self.eval_expr(current_element.strip()))
                                    
                                    self.variables[var_name.strip()] = elements
                                else:
                                    self.variables[var_name.strip()] = []
                        else:
                            value = self.eval_expr(expr)
                            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            self.variables[var_name.strip()] = value
                    else:
                        self.variables[var_part.strip(" ;")] = 0
                
                elif line.startswith("if "):
                    # Handle if statements: if x > 5: { ... } else: { ... }
                    if_match = re.search(r'if\s+(.+?):', line)
                    if if_match:
                        condition = if_match.group(1).strip()
                        condition_result = self.eval_expr(condition)
                        
                        # Check if this is a block or single statement
                        if '{' in line or (i + 1 < len(lines) and '{' in lines[i + 1]):
                            # Block syntax
                            if_body = self.parse_function_body(lines, i)
                            end_i = self.find_function_end(lines, i)
                            
                            # Check for else clause
                            else_body = []
                            if end_i < len(lines) and lines[end_i].strip().startswith("else"):
                                else_body = self.parse_function_body(lines, end_i)
                                end_i = self.find_function_end(lines, end_i)
                            
                            # Execute appropriate branch
                            if condition_result:
                                self.execute(if_body)
                            elif else_body:
                                self.execute(else_body)
                            
                            i = end_i
                            continue
                        else:
                            # Single statement syntax
                            if condition_result and i + 1 < len(lines):
                                next_line = lines[i + 1].strip()
                                try:
                                    self.execute([next_line])
                                except StopIteration as ctrl:
                                    raise ctrl  # Re-raise break/continue
                            i += 2
                            continue
                
                elif line.startswith("while "):
                    # Handle while loops: while x < 10: { ... }
                    while_match = re.search(r'while\s+(.+?):', line)
                    if while_match:
                        condition = while_match.group(1).strip()
                        
                        # Parse the loop body
                        body = self.parse_function_body(lines, i)
                        
                        # Execute the loop
                        while self.eval_expr(condition):
                            try:
                                self.execute(body)
                            except StopIteration as ctrl:
                                if ctrl.args[0] == "BREAK":
                                    break
                                elif ctrl.args[0] == "CONTINUE":
                                    continue
                            except Exception as e:
                                self.error(f"Error in while loop: {str(e)}")
                                break
                        
                        # Skip to end of loop
                        i = self.find_function_end(lines, i)
                        continue
                
                elif line.startswith("for "):
                    # Handle for loops: for (summon i = 0; i < 5; i = i + 1): { ... }
                    for_match = re.search(r'for\s*\((.+?)\):', line)
                    if for_match:
                        content = for_match.group(1)
                        parts = [part.strip() for part in content.split(";")]
                        
                        if len(parts) == 3:
                            init, cond, step = parts
                            
                            # Execute initialization (remove summon if present)
                            if init.startswith("summon"):
                                init = init[6:].strip()
                            self.execute([init])
                            
                            # Parse the loop body
                            body = self.parse_function_body(lines, i)
                            
                            # Execute the loop
                            while self.eval_expr(cond):
                                try:
                                    self.execute(body)
                                except StopIteration as ctrl:
                                    if ctrl.args[0] == "BREAK":
                                        break
                                    elif ctrl.args[0] == "CONTINUE":
                                        continue
                                except Exception as e:
                                    self.error(f"Error in for loop: {str(e)}")
                                    break
                                
                                # Execute step
                                self.execute([step])
                            
                            # Skip to end of loop
                            i = self.find_function_end(lines, i)
                            continue
                
                elif line.startswith("stride "):
                    # Handle stride loops: stride i from 0 to 10: { ... }
                    stride_match = re.search(r'stride\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+?):', line)
                    if stride_match:
                        var_name = stride_match.group(1)
                        start_val = stride_match.group(2).strip()
                        end_val = stride_match.group(3).strip()
                        
                        # Evaluate start and end values
                        start = self.eval_expr(start_val)
                        end = self.eval_expr(end_val)
                        
                        # Parse the loop body
                        body = self.parse_function_body(lines, i)
                        
                        # Execute the loop
                        old_var_value = self.variables.get(var_name)
                        self.variables[var_name] = start
                        
                        while self.variables[var_name] <= end:
                            try:
                                self.execute(body)
                            except StopIteration as ctrl:
                                if ctrl.args[0] == "BREAK":
                                    break
                                elif ctrl.args[0] == "CONTINUE":
                                    continue
                            except Exception as e:
                                self.error(f"Error in stride loop: {str(e)}")
                                break
                            
                            # Increment the variable
                            self.variables[var_name] += 1
                        
                        # Restore original variable value
                        if old_var_value is not None:
                            self.variables[var_name] = old_var_value
                        elif var_name in self.variables:
                            del self.variables[var_name]
                        
                        # Skip to end of loop
                        i = self.find_function_end(lines, i)
                        continue
                
                elif line == "break" or line == "break;":
                    raise StopIteration("BREAK")
                elif line == "continue" or line == "continue;":
                    raise StopIteration("CONTINUE")
                elif line.startswith("return"):
                    # Handle return statements
                    if line == "return" or line == "return;":
                        raise ReturnException(None)
                    else:
                        return_expr = line[6:].strip(" ;")
                        return_value = self.eval_expr(return_expr)
                        raise ReturnException(return_value)
                
                else:
                    # Variable assignment (without summon)
                    if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=', '<', '>']):
                        var_name, expr = line.split('=', 1)
                        var_name = var_name.strip()
                        expr = expr.strip(' ;')
                        
                        # Handle swapping: a, b = b, a
                        if ',' in var_name:
                            var_names = [v.strip() for v in var_name.split(',')]
                            if ',' in expr:
                                # Multiple assignment: a, b = c, d
                                expr_parts = [e.strip() for e in expr.split(',')]
                                if len(var_names) == len(expr_parts):
                                    # Evaluate all expressions first (for swapping)
                                    values = [self.eval_expr(e) for e in expr_parts]
                                    # Then assign them
                                    for var, val in zip(var_names, values):
                                        self.variables[var] = val
                                else:
                                    self.error(f"Mismatch in assignment: {len(var_names)} variables, {len(expr_parts)} values")
                            else:
                                self.error("Multiple variables require multiple values")
                        else:
                            # Single assignment
                            value = self.eval_expr(expr)
                            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            self.variables[var_name] = value
            
            except StopIteration as ctrl:
                # Re-raise break/continue for loops to handle
                raise ctrl
            except ReturnException as ret:
                # Re-raise return for functions to handle
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
        
        print(f"🚀 Running Enhanced Soutk program: {filename}")
        print("=" * 50)
        
        interpreter = SoutkInterpreter()
        interpreter.execute(code)
        
        print("=" * 50)
        print("✅ Program completed successfully!")
        
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")

if __name__ == "__main__":
    main()
