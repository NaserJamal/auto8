# auto8/auto8/fixers/e127_continuation_line_over_indented.py
import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num > 1 and line_num <= len(lines):
        previous_line = lines[line_num - 2].rstrip('\n')
        current_line = lines[line_num - 1].rstrip('\n')

        # Find the position of the first opening parenthesis in the previous line
        first_paren_pos = previous_line.find('(')
        
        if first_paren_pos != -1:
            # Calculate the correct indentation
            correct_indent = ' ' * (first_paren_pos + 1)
            
            # Case 1: Previous line ends with '//' or other operator
            if re.search(r'[+\-*/]=?\s*$', previous_line) or previous_line.rstrip().endswith('//'):
                current_indent = len(current_line) - len(current_line.lstrip())
                if current_indent != len(correct_indent):
                    fixed_line = correct_indent + current_line.lstrip()
                    lines[line_num - 1] = fixed_line + '\n'

            # Case 2: Current line contains '//' or starts with an operator
            elif '//' in current_line or re.match(r'\s*[+\-*/]', current_line):
                current_indent = len(current_line) - len(current_line.lstrip())
                if current_indent != len(correct_indent):
                    fixed_line = correct_indent + current_line.lstrip()
                    lines[line_num - 1] = fixed_line + '\n'

            # Case 3: Other continuation lines
            else:
                nested_paren_match = re.search(r'\([^()]*\)$', previous_line)
                if nested_paren_match:
                    correct_indent = ' ' * (first_paren_pos + 1)
                    current_indent = len(current_line) - len(current_line.lstrip())
                    if current_indent != len(correct_indent):
                        fixed_line = correct_indent + current_line.lstrip()
                        lines[line_num - 1] = fixed_line + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)