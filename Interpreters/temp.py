"""
Soutk MVP Interpreter - Fixed Version
A minimal but functional Python-based interpreter for the custom Soutk language.
"""

import re
from pathlib import Path

class SoutkInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}  # Store function definitions
        self.line_number = 0
        self.processed_lines = set()  # Track which lines have been processed

    
    def error(self, message):
        """Display error with line number"""
        print(f"⌐ Line {self.line_number}: {message}")
    
    def eval_expr(self, expr):
        """Evaluate expressions safely - FIXED VERSION"""
        expr = expr.strip()
        if not expr:
            return ""
        
        # Handle string literals first
        string_literals = []
        def replace_strings(match):
            string_literals.append(match.group(0))
            return f"__STRING_{len(string_literals)-1}__"
        
        # Capture both double and single quoted strings
        expr = re.sub(r'"[^"]*"', replace_strings, expr)
        expr = re.sub(r"'[^']*'", replace_strings, expr)
        
        # Handle array access: array[index] - do this before variable replacement
        array_access_pattern = r'(\w+)\[([^\]]+)\]'
        def replace_array_access(match):
            array_name = match.group(1)
            index_expr = match.group(2)
            
            if array_name in self.variables:
                array = self.variables[array_name]
                if isinstance(array, list):
                    try:
                        index = self.eval_expr(index_expr)
                        if isinstance(index, int) and 0 <= index < len(array):
                            return str(array[index])
                        else:
                            raise ValueError(f"Array index {index} out of bounds")
                    except:
                        raise ValueError(f"Invalid array index: {index_expr}")
                else:
                    raise ValueError(f"'{array_name}' is not an array")
            else:
                raise ValueError(f"Array '{array_name}' not defined")
        
        expr = re.sub(array_access_pattern, replace_array_access, expr)
        
        # Replace variables with their values - IMPROVED
        # Sort variables by length (longest first) to avoid partial replacements
        for var_name in sorted(self.variables.keys(), key=len, reverse=True):
            var_value = self.variables[var_name]
            # Use word boundaries to avoid partial replacements
            pattern = rf'\b{re.escape(var_name)}\b'
            if re.search(pattern, expr):
                if isinstance(var_value, str):
                    # Don't add quotes if it's already a quoted string
                    if not (var_value.startswith('"') and var_value.endswith('"')):
                        replacement = f'"{var_value}"'
                    else:
                        replacement = var_value
                elif isinstance(var_value, bool):
                    replacement = "True" if var_value else "False"
                else:
                    replacement = str(var_value)
                expr = re.sub(pattern, replacement, expr)
        
        # Restore string literals
        for i, literal in enumerate(string_literals):
            expr = expr.replace(f"__STRING_{i}__", literal)
        
        # Handle logical operators - IMPROVED
        expr = expr.replace("&&", " and ").replace("||", " or ")
        expr = expr.replace(" not ", " not ")  # Ensure proper spacing
        
        # Handle boolean literals
        expr = expr.replace("true", "True").replace("false", "False")
        
        try:
            # Check if this is a string concatenation or mathematical operation
            # If there are quotes in the expression, it's likely string concatenation
            has_strings = '"' in expr or "'" in expr
            
            if '+' in expr:
                # Split by + and evaluate each part
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
                        quote_char = None
                        current_part += char
                    elif char == '(' and not in_quotes:
                        paren_depth += 1
                        current_part += char
                    elif char == ')' and not in_quotes:
                        paren_depth -= 1
                        current_part += char
                    elif char == '+' and not in_quotes and paren_depth == 0:
                        parts.append(current_part.strip())
                        current_part = ""
                    else:
                        current_part += char
                
                if current_part.strip():
                    parts.append(current_part.strip())
                
                if len(parts) > 1:
                    # Evaluate each part
                    evaluated_parts = []
                    for part in parts:
                        if part:
                            try:
                                # If it's a simple quoted string, use as-is
                                if part.startswith('"') and part.endswith('"'):
                                    evaluated_parts.append(part[1:-1])
                                elif part.startswith("'") and part.endswith("'"):
                                    evaluated_parts.append(part[1:-1])
                                else:
                                    # Try to evaluate as expression first
                                    try:
                                        safe_dict = {
                                            "__builtins__": {"len": len, "str": str, "int": int, "float": float},
                                            "True": True,
                                            "False": False
                                        }
                                        result = eval(part, safe_dict)
                                        evaluated_parts.append(result)
                                    except:
                                        # If evaluation fails, treat as string
                                        evaluated_parts.append(part)
                            except:
                                evaluated_parts.append(part)
                    
                    # Determine if we should concatenate as strings or add as numbers
                    if any(isinstance(p, str) for p in evaluated_parts):
                        # String concatenation
                        result = ""
                        for part in evaluated_parts:
                            result += str(part)
                        return result
                    else:
                        # Numeric addition
                        result = 0
                        for part in evaluated_parts:
                            try:
                                result += float(part) if isinstance(part, (int, float)) else 0
                            except:
                                result += 0
                        return int(result) if result.is_integer() else result
            
            # Handle other operators and expressions
            safe_dict = {
                "__builtins__": {"len": len, "str": str, "int": int, "float": float},
                "True": True,
                "False": False
            }
            
            result = eval(expr, safe_dict)
            return result
            
        except Exception as e:
            # If evaluation fails completely, return the original expression
            # This helps with debugging
            print(f"DEBUG: Expression evaluation failed for '{expr}': {str(e)}")
            return expr
    
    def parse_block(self, lines, start):
        """Parse code blocks between { and }"""
        block = []
        depth = 0
        i = start
        
        while i < len(lines):
            line = lines[i].strip()
            
            if '{' in line:
                depth += line.count('{')
                if depth == 1:
                    i += 1
                    continue
            
            if '}' in line:
                depth -= line.count('}')
                if depth == 0:
                    i += 1
                    break
            
            if depth >= 1:
                block.append(line)
            
            i += 1
        
        return block, i
    
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
            
            # Skip lines that have been processed as part of function definitions
            if i in self.processed_lines:
                i += 1
                continue
            
            try:
                if line.startswith("summon "):
                    i = self.handle_summon(lines, i)
                elif line.startswith("chant"):
                    i = self.handle_chant(lines, i)
                elif line.startswith("if "):
                    i = self.handle_if(lines, i)
                elif line.startswith("while "):
                    i = self.handle_while(lines, i)
                elif line.startswith("do"):
                    i = self.handle_do_while(lines, i)
                elif line.startswith("for "):
                    i = self.handle_for(lines, i)
                elif line.startswith("stride "):
                    i = self.handle_stride(lines, i)
                elif line.startswith("spell"):
                    i = self.handle_spell(lines, i)
                elif line.startswith("cast "):
                    i = self.handle_cast(lines, i)
                elif line == "break;":
                    raise StopIteration("BREAK")
                elif line == "continue;":
                    raise StopIteration("CONTINUE")
                elif line.startswith("else"):
                    i += 1  # Skip else lines as they're handled in if statements
                    continue
                else:
                    # Variable assignment
                    if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=', '<', '>']):
                        var_name, expr = line.split('=', 1)
                        self.variables[var_name.strip()] = self.eval_expr(expr.strip(' ;'))
                        i += 1
                        continue
            except StopIteration as loop_control:
                raise loop_control
            except Exception as e:
                self.error(str(e))
                i += 1
                continue
            
            i += 1
    
    def handle_summon(self, lines, i):
        """Handle variable declaration: summon x = 5 or summon arr = [1, 2, 3]"""
        line = lines[i]
        var_part = line[7:].strip()  # Remove "summon "
        
        if '=' in var_part:
            var_name, expr = var_part.split("=", 1)
            expr = expr.strip(" ;")
            
            # Handle array creation: [1, 2, 3]
            if expr.startswith('[') and expr.endswith(']'):
                array_content = expr[1:-1].strip()
                if array_content:
                    # Parse array elements
                    elements = []
                    current_element = ""
                    in_quotes = False
                    quote_char = None
                    
                    for char in array_content:
                        if char in ['"', "'"] and not in_quotes:
                            in_quotes = True
                            quote_char = char
                            current_element += char
                        elif char == quote_char and in_quotes:
                            in_quotes = False
                            current_element += char
                        elif char == ',' and not in_quotes:
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
                # Don't strip quotes from already processed strings
                self.variables[var_name.strip()] = value
        else:
            self.variables[var_part.strip(" ;")] = 0
        
        return i + 1
    
    def handle_chant(self, lines, i):
        """Handle output: chant "Hello" or chant(x)"""
        line = lines[i]
        
        if line.startswith("chant "):
            to_print = line[6:].strip(" ;")
        elif line.startswith("chant("):
            to_print = line[5:].strip(" ;")
        else:
            to_print = line[5:].strip(" ;")
        
        result = self.eval_expr(to_print)
        
        # Handle the output properly
        if isinstance(result, str):
            # Remove quotes only if they were added by our evaluation
            if result.startswith('"') and result.endswith('"') and len(result) > 2:
                result = result[1:-1]
        
        print(result)
        return i + 1
    
    def handle_if(self, lines, i):
        """Handle if statements: if x > 5: { ... } else: { ... }"""
        line = lines[i]
        
        # Parse condition: if x > 5: or if (x > 5):
        if_match = re.search(r'if\s*(?:\((.*?)\)|(.*?)):', line)
        if not if_match:
            self.error(f"Invalid if statement syntax: {line}")
            return i + 1
        
        condition = if_match.group(1) or if_match.group(2)
        condition_result = self.eval_expr(condition)
        
        # Convert result to boolean
        if isinstance(condition_result, str):
            condition_result = condition_result.lower() not in ['false', '', '0']
        
        if condition_result:
            if '{' in line:
                block, end_i = self.parse_block(lines, i)
                self.execute(block)
                # Skip else block if it exists
                if end_i < len(lines) and lines[end_i].strip().startswith("else"):
                    if '{' in lines[end_i]:
                        _, end_i = self.parse_block(lines, end_i)
                return end_i
            else:
                if i + 1 < len(lines):
                    self.execute([lines[i + 1]])
                return i + 2
        else:
            if '{' in line:
                block, end_i = self.parse_block(lines, i)
                # Look for else clause
                if end_i < len(lines) and lines[end_i].strip().startswith("else"):
                    else_line = lines[end_i].strip()
                    if '{' in else_line:
                        block, end_i = self.parse_block(lines, end_i)
                        self.execute(block)
                        return end_i
                    else:
                        if end_i + 1 < len(lines):
                            self.execute([lines[end_i + 1]])
                        return end_i + 2
                return end_i
            else:
                return i + 2
    
    def handle_while(self, lines, i):
        """Handle while loops: while x < 10: { ... }"""
        line = lines[i]
        
        # Parse condition: while x < 10: or while (x < 10):
        while_match = re.search(r'while\s*(?:\((.*?)\)|(.*?)):', line)
        if not while_match:
            self.error(f"Invalid while statement syntax: {line}")
            return i + 1
        
        condition = while_match.group(1) or while_match.group(2)
        
        if '{' in line:
            block, end_i = self.parse_block(lines, i)
            while self.eval_expr(condition):
                try:
                    self.execute(block)
                except StopIteration as ctrl:
                    if ctrl.args[0] == "BREAK":
                        break
                    elif ctrl.args[0] == "CONTINUE":
                        continue
            return end_i
        else:
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                while self.eval_expr(condition):
                    self.execute([next_line])
            return i + 2
    
    def handle_do_while(self, lines, i):
        """Handle do-while loops: do { ... } while (x < 10)"""
        if '{' in lines[i]:
            block, end_i = self.parse_block(lines, i)
            
            if end_i < len(lines):
                while_line = lines[end_i].strip()
                condition_match = re.search(r'while\s*\((.*?)\)', while_line)
                if condition_match:
                    condition = condition_match.group(1)
                    while True:
                        try:
                            self.execute(block)
                        except StopIteration as ctrl:
                            if ctrl.args[0] == "BREAK":
                                break
                            elif ctrl.args[0] == "CONTINUE":
                                continue
                        
                        if not self.eval_expr(condition):
                            break
                    
                    return end_i + 1
        
        return i + 1
    
    def handle_for(self, lines, i):
        """Handle for loops: for (summon i = 0; i < 5; i = i + 1): { ... }"""
        line = lines[i]
        content_match = re.search(r'\((.*?)\)', line)
        if not content_match:
            self.error(f"Invalid for statement syntax: {line}")
            return i + 1
        
        content = content_match.group(1)
        parts = [part.strip() for part in content.split(";")]
        
        if len(parts) != 3:
            self.error("For loop must have 3 parts: init; condition; increment")
            return i + 1
        
        init, cond, step = parts
        
        # Execute initialization
        if init.startswith("summon"):
            self.execute([init])
        else:
            self.execute([f"summon {init}"])
        
        if '{' in line:
            block, end_i = self.parse_block(lines, i)
            while self.eval_expr(cond):
                try:
                    self.execute(block)
                except StopIteration as ctrl:
                    if ctrl.args[0] == "BREAK":
                        break
                    elif ctrl.args[0] == "CONTINUE":
                        continue
                
                self.execute([step])
            
            return end_i
        else:
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                while self.eval_expr(cond):
                    self.execute([next_line])
                    self.execute([step])
            
            return i + 2
    
    def handle_stride(self, lines, i):
        """Handle stride loops: stride i from 0 to 10: { ... }"""
        line = lines[i]
        
        # Parse: stride i from 0 to 10:
        stride_match = re.search(r'stride\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+?):', line)
        if not stride_match:
            self.error(f"Invalid stride statement syntax: {line}")
            return i + 1
        
        var_name = stride_match.group(1)
        start_val = stride_match.group(2).strip()
        end_val = stride_match.group(3).strip()
        
        # Evaluate start and end values
        start = self.eval_expr(start_val)
        end = self.eval_expr(end_val)
        
        # Convert to integers if they're numeric
        try:
            start = int(start) if isinstance(start, (int, float)) else start
            end = int(end) if isinstance(end, (int, float)) else end
        except:
            pass
        
        # Initialize the variable
        self.variables[var_name] = start
        
        # Parse the block
        block, end_i = self.parse_block(lines, i)
        
        # Execute the loop
        while self.variables[var_name] <= end:
            try:
                self.execute(block)
            except StopIteration as ctrl:
                if ctrl.args[0] == "BREAK":
                    break
                elif ctrl.args[0] == "CONTINUE":
                    self.variables[var_name] += 1
                    continue
            
            # Increment the variable
            self.variables[var_name] += 1
        
        return end_i

    def handle_spell(self, lines, i):
        """Handle function definition: spell greet(name): { ... }"""
        line = lines[i]
        
        # Parse: spell function_name(param1, param2): or spell function_name(param1):
        spell_match = re.search(r'spell\s+(\w+)\s*\((.*?)\):', line)
        if not spell_match:
            self.error(f"Invalid spell statement syntax: {line}")
            return i + 1
        
        func_name = spell_match.group(1)
        params_str = spell_match.group(2).strip()
        
        # Parse parameters
        if params_str:
            params = [param.strip() for param in params_str.split(',')]
        else:
            params = []
        
        # Parse the function body
        block, end_i = self.parse_block(lines, i)
        
        # Mark function body lines as processed so they don't get executed
        for j in range(i + 1, end_i):
            self.processed_lines.add(j)
        
        # Store the function
        self.functions[func_name] = {
            'params': params,
            'body': block
        }
        
        return end_i
    
    def handle_cast(self, lines, i):
        """Handle function call: cast greet("World")"""
        line = lines[i]
        
        # Parse: cast function_name(arg1, arg2) or cast function_name()
        cast_match = re.search(r'cast\s+(\w+)\s*\((.*?)\)', line)
        if not cast_match:
            self.error(f"Invalid cast statement syntax: {line}")
            return i + 1
        
        func_name = cast_match.group(1)
        args_str = cast_match.group(2).strip()
        
        # Check if function exists
        if func_name not in self.functions:
            self.error(f"Function '{func_name}' not defined")
            return i + 1
        
        func = self.functions[func_name]
        params = func['params']
        body = func['body']
        
        # Parse arguments
        args = []
        if args_str:
            # Simple argument parsing - split by comma but respect quotes
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
        if len(args) != len(params):
            self.error(f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}")
            return i + 1
        
        # Create temporary scope
        old_variables = self.variables.copy()
        
        # Set parameters
        for param, arg in zip(params, args):
            self.variables[param] = self.eval_expr(arg)
        
        # Execute function body
        try:
            self.execute(body)
        except Exception as e:
            self.error(f"Error in function '{func_name}': {str(e)}")
        finally:
            # Restore original variables
            self.variables = old_variables
        
        return i + 1

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
            print(f"⌐ Error: File '{filename}' not found.")
            return
        
        with open(file_path, "r", encoding='utf-8') as f:
            code = f.read()
        
        print(f"🚀 Running Soutk program: {filename}")
        print("=" * 50)
        
        interpreter = SoutkInterpreter()
        interpreter.execute(code)
        
        print("=" * 50)
        print("✅ Program completed successfully!")
        
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")

if __name__ == "__main__":
    main()