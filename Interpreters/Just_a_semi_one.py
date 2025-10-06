
import re
from pathlib import Path

class SoutkInterpreter:
    def __init__(self):
        self.variables = {}

    def listen(self, prompt=""):
        try:
            if prompt:
                if isinstance(prompt, str) and prompt.startswith('"') and prompt.endswith('"'):
                    prompt = prompt[1:-1]
                return input(prompt)
            else:
                return input()
        except KeyboardInterrupt:
            return ""
        except EOFError:
            return ""

    def eval_expr(self, expr):
        expr = expr.strip()

        # Handle string literals
        string_literals = []
        def replace_strings(match):
            string_literals.append(match.group(0))
            return f"__STRING_{len(string_literals)-1}__"

        expr = re.sub(r'"[^"]*"', replace_strings, expr)
        expr = re.sub(r"'[^']*'", replace_strings, expr)

        # Replace variables
        for var in sorted(self.variables, key=len, reverse=True):
            if var in expr:
                var_value = self.variables[var]
                if isinstance(var_value, str):
                    replacement = f'"{var_value}"' if not (var_value.startswith('"') and var_value.endswith('"')) else var_value
                else:
                    replacement = str(var_value)
                expr = re.sub(rf'\b{re.escape(var)}\b', replacement, expr)

        # Restore string literals
        for i, literal in enumerate(string_literals):
            expr = expr.replace(f"__STRING_{i}__", literal)

        # Handle logical operators
        expr = expr.replace("&&", "and").replace("||", "or")

        try:
            # Handle string concatenation with + operator
            if '+' in expr and not any(op in expr for op in ['==', '!=', '<=', '>=', '<', '>']):
                parts = expr.split('+')
                if len(parts) > 1:
                    # Evaluate each part separately and concatenate
                    evaluated_parts = []
                    for part in parts:
                        part = part.strip()
                        if part:  # Skip empty parts
                            try:
                                evaluated_parts.append(self.eval_expr(part))
                            except:
                                evaluated_parts.append(part)
                    # Convert all parts to strings and concatenate
                    result = ""
                    for part in evaluated_parts:
                        if isinstance(part, str):
                            if part.startswith('"') and part.endswith('"'):
                                result += part[1:-1]
                            else:
                                result += part
                        else:
                            result += str(part)
                    return result
            
            safe_dict = {
                "__builtins__": {"len": len, "str": str, "int": int, "float": float, "listen": self.listen},
                "true": True,
                "false": False
            }
            return eval(expr, safe_dict)
        except Exception as e:
            raise ValueError(f"Invalid expression: {expr} - {str(e)}")

    def parse_block(self, lines, start):
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
                    i += 1  # Move past the closing brace
                    break
            
            if depth >= 1:
                block.append(line)
            
            i += 1
        
        return block, i

    def execute(self, code):
        if isinstance(code, str):
            lines = [line.strip() for line in code.splitlines() if line.strip() and not line.strip().startswith('//')]
        else:
            lines = code

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            try:
                if line.startswith("summon "):
                    self.handle_summon(line)
                elif line.startswith("chant"):
                    self.handle_chant(line)
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
                elif line == "break;":
                    raise StopIteration("BREAK")
                elif line == "continue;":
                    raise StopIteration("CONTINUE")
                elif line.startswith("else"):
                    pass
                else:
                    if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
                        var_name, expr = line.split('=', 1)
                        self.variables[var_name.strip()] = self.eval_expr(expr.strip(' ;'))
            except StopIteration as loop_control:
                raise loop_control
            except Exception as e:
                print(f"⚠️  Line {i+1}: {line}")
                print(f"🛑 Error: {str(e)}")
            
            i += 1

    def handle_summon(self, line):
        var_part = line[len("summon "):].strip()
        if '=' in var_part:
            var_name, expr = var_part.split("=", 1)
            value = self.eval_expr(expr.strip(" ;"))
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            self.variables[var_name.strip()] = value
        else:
            self.variables[var_part.strip(" ;")] = 0

    def handle_chant(self, line):
        # Handle both "chant " and "chant(" cases
        if line.startswith("chant "):
            to_print = line[6:].strip(" ;")
        elif line.startswith("chant("):
            to_print = line[5:].strip(" ;")
        else:
            # Fallback for any other chant format
            to_print = line[5:].strip(" ;")
        
        result = self.eval_expr(to_print)
        if isinstance(result, str) and result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        print(result)

    def handle_if(self, lines, i):
        line = lines[i]
        # Parse: if condition: or if (condition):
        if_match = re.search(r'if\s*(?:\((.*?)\)|(.*?)):', line)
        if not if_match:
            raise ValueError(f"Invalid if statement syntax: {line}")
        
        condition = if_match.group(1) or if_match.group(2)
        condition_result = self.eval_expr(condition)
        
        if condition_result:
            if '{' in line:
                block, end_i = self.parse_block(lines, i)
                self.execute(block)
                return end_i
            else:
                if i + 1 < len(lines):
                    self.execute([lines[i + 1]])
                return i + 1
        else:
            if '{' in line:
                block, end_i = self.parse_block(lines, i)
                i = end_i + 1
            else:
                i += 2
            
            if i < len(lines) and lines[i].strip().startswith("else"):
                else_line = lines[i].strip()
                if '{' in else_line:
                    block, end_i = self.parse_block(lines, i)
                    self.execute(block)
                    return end_i
                else:
                    if i + 1 < len(lines):
                        self.execute([lines[i + 1]])
                    return i + 1
            else:
                return i - 1

    def handle_while(self, lines, i):
        line = lines[i]
        # Parse: while condition: or while (condition):
        while_match = re.search(r'while\s*(?:\((.*?)\)|(.*?)):', line)
        if not while_match:
            raise ValueError(f"Invalid while statement syntax: {line}")
        
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
            return i + 1

    def handle_do_while(self, lines, i):
        if '{' in lines[i]:
            block, end_i = self.parse_block(lines, i)
            while_line_i = end_i + 1
            
            if while_line_i < len(lines):
                while_line = lines[while_line_i].strip()
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
                    
                    return while_line_i
        return i

    def handle_for(self, lines, i):
        line = lines[i]
        content_match = re.search(r'\((.*?)\)', line)
        if not content_match:
            raise ValueError(f"Invalid for statement syntax: {line}")
        
        content = content_match.group(1)
        parts = [part.strip() for part in content.split(";")]
        
        if len(parts) != 3:
            raise ValueError(f"For loop must have 3 parts: init; condition; increment")
        
        init, cond, step = parts
        
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
            
            return i + 1

    def handle_stride(self, lines, i):
        line = lines[i]
        
        # Parse: stride i from 0 to 10:
        stride_match = re.search(r'stride\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+?):', line)
        if not stride_match:
            raise ValueError(f"Invalid stride statement syntax: {line}")
        
        var_name = stride_match.group(1)
        start_val = stride_match.group(2).strip()
        end_val = stride_match.group(3).strip()
        
        # Evaluate start and end values
        start = self.eval_expr(start_val)
        end = self.eval_expr(end_val)
        
        # Initialize the variable
        self.variables[var_name] = start
        
        # Always look for a block after stride, since the syntax requires it
        block, end_i = self.parse_block(lines, i)
        
        while self.variables[var_name] <= end:
            try:
                self.execute(block)
            except StopIteration as ctrl:
                if ctrl.args[0] == "BREAK":
                    break
                elif ctrl.args[0] == "CONTINUE":
                    continue
            
            # Increment the variable
            self.variables[var_name] += 1
        
        return end_i

def main():
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "hello.stk"
    
    try:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"Error: File '{filename}' not found.")
            return
        
        with open(file_path, "r") as f:
            code = f.read()
        
        interpreter = SoutkInterpreter()
        interpreter.execute(code)
    except Exception as e:
        print(f"Error running program: {str(e)}")

if __name__ == "__main__":
    main()
