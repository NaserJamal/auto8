# auto8/auto8/fixers/e501_line_too_long.py
import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num <= len(lines):
        original_line = lines[line_num - 1].rstrip('\n')
        indent = len(original_line) - len(original_line.lstrip())
        
        # Case 1: Check for long print statements
        print_match = re.match(r'(\s*)(print\(")(.*)("\))\s*$', original_line)
        if print_match and len(original_line) > 79:
            indent_str, print_start, content, print_end = print_match.groups()
            max_line_length = 79 - len(indent_str) - len(print_start) - 1  # -1 for the backslash
            
            new_lines = []
            current_line = indent_str + print_start
            
            words = content.split()
            for word in words:
                if len(current_line) + len(word) + 1 <= max_line_length:
                    current_line += word + ' '
                else:
                    new_lines.append(current_line.rstrip() + ' \\')
                    current_line = indent_str + ' ' * (len(print_start) - 1)  # Align with opening quote
                    current_line += word + ' '
            
            new_lines.append(current_line.rstrip() + print_end)
            
            lines[line_num - 1:line_num] = [line + '\n' for line in new_lines]
        
        # Case 2: Check for long string literals
        elif re.match(r'(\s*)(["\'])(.*)\2\s*$', original_line) and len(original_line) > 79:
            indent_str, quote, content = re.match(r'(\s*)(["\'])(.*)\2\s*$', original_line).groups()
            max_line_length = 79 - len(indent_str) - 1  # -1 for the backslash
            
            new_lines = []
            current_line = indent_str + quote
            
            words = content.split()
            for word in words:
                if len(current_line) + len(word) + 1 <= max_line_length:
                    current_line += word + ' '
                else:
                    new_lines.append(current_line.rstrip() + ' \\')
                    current_line = indent_str
                    current_line += word + ' '
            
            new_lines.append(current_line.rstrip() + quote)
            
            lines[line_num - 1:line_num] = [line + '\n' for line in new_lines]
        
        # Case 3: Other long lines (existing cases)
        elif len(original_line) > 79:
            # Check if the line is a simple assignment
            assignment_match = re.match(r'^(\s*)(.+?=\s*)(.+)$', original_line)
            if assignment_match:
                before_eq, eq_part, after_eq = assignment_match.groups()
                new_lines = [
                    f"{before_eq}{eq_part}(\n",
                    f"{' ' * (indent + 4)}{after_eq.strip()}\n",
                    f"{' ' * indent})\n"
                ]
                lines[line_num - 1:line_num] = new_lines
            else:
                # Handle lines that are not function calls or assignments
                words = original_line.split()
                new_lines = []
                current_line = ' ' * indent
                for word in words:
                    if len(current_line) + len(word) + 1 <= 79:
                        current_line += word + ' '
                    else:
                        new_lines.append(current_line.rstrip())
                        current_line = ' ' * indent + word + ' '
                
                new_lines.append(current_line.rstrip())
                lines[line_num - 1] = '\n'.join(new_lines) + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)