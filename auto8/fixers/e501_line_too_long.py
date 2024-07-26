# auto8/auto8/fixers/e501_line_too_long.py
import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num <= len(lines):
        original_line = lines[line_num - 1].rstrip('\n')
        indent = len(original_line) - len(original_line.lstrip())
        
        # New case: Check for long string literals
        string_match = re.match(r'(\s*)(["\'])(.*)\2\s*$', original_line)
        if string_match and len(original_line) > 79:
            indent_str, quote, content = string_match.groups()
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
        
        # Existing cases
        elif re.match(r'^(\s*)(.+?=\s*)(.+)$', original_line) and len(original_line) > 79:
            # Handle simple assignment case
            before_eq, eq_part, after_eq = re.match(r'^(\s*)(.+?=\s*)(.+)$', original_line).groups()
            new_lines = [
                f"{before_eq}{eq_part}(\n",
                f"{' ' * (indent + 4)}{after_eq.strip()}\n",
                f"{' ' * indent})\n"
            ]
            lines[line_num - 1:line_num] = new_lines
        elif len(original_line) > 79:
            # Check if the line starts with a function call or complex assignment
            match = re.match(r'^(\s*)(\w+\s*=\s*)?(\w+\()(.*)(\))$', original_line)
            if match:
                prefix = match.group(1) + (match.group(2) or '') + match.group(3)
                content = match.group(4)
                suffix = match.group(5)
                
                # Split the content
                words = content.split()
                new_lines = [prefix]
                current_line = ' ' * (indent + 4)
                
                for word in words:
                    if len(current_line) + len(word) + 1 <= 79 - len(suffix):
                        current_line += word + ' '
                    else:
                        new_lines.append(current_line.rstrip())
                        current_line = ' ' * (indent + 4) + word + ' '
                
                new_lines.append(current_line.rstrip() + suffix)
                lines[line_num - 1] = '\n'.join(new_lines) + '\n'
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