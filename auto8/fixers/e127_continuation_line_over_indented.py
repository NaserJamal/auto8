# auto8/auto8/fixers/e127_continuation_line_over_indented.py
import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num > 1 and line_num <= len(lines):
        previous_line = lines[line_num - 2].rstrip('\n')
        current_line = lines[line_num - 1].rstrip('\n')

        # Check if the previous line contains a pattern like "(... - ...)"
        nested_paren_match = re.search(r'\([^()]*-[^()]*\)$', previous_line)
        if nested_paren_match:
            # Find the position of the first opening parenthesis in the expression
            opening_paren_pos = previous_line.find('(')
            
            # Calculate the correct indentation
            correct_indent = ' ' * (opening_paren_pos + 1)
            
            # Check if the current line starts with '//' and is over-indented
            if current_line.lstrip().startswith('//'):
                current_indent = len(current_line) - len(current_line.lstrip())
                if current_indent > len(correct_indent):
                    # Fix the indentation
                    fixed_line = correct_indent + current_line.lstrip()
                    lines[line_num - 1] = fixed_line + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)