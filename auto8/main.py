# auto8/auto8/main.py

import subprocess
import re
import sys
from pathlib import Path
from auto8.fixers import (
    e501_line_too_long,
    w292_no_newline_at_eof,
    e502_redundant_backslash,
    w291_trailing_whitespace,
    w293_blank_line_whitespace
)
def run_flake8(file_path=None):
    command = ['flake8']
    if file_path:
        command.append(file_path)
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def parse_flake8_output(output):
    pattern = r'(.+):(\d+):(\d+): (\w+) (.+)'
    issues = []
    for line in output.split('\n'):
        match = re.match(pattern, line)
        if match:
            file_path, line_num, col_num, error_code, description = match.groups()
            issues.append({
                'file_path': file_path,
                'line_num': int(line_num),
                'col_num': int(col_num),
                'error_code': error_code,
                'description': description
            })
    return issues

def fix_issues(issues):
    for issue in issues:
        if issue['error_code'] == 'E501':
            e501_line_too_long.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'W292':
            w292_no_newline_at_eof.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'E502':
            e502_redundant_backslash.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'W291':
            w291_trailing_whitespace.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'W293':
            w293_blank_line_whitespace.fix(issue['file_path'], issue['line_num'])
        # Add more fixers for other error codes

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        flake8_output = run_flake8(file_path)
    else:
        flake8_output = run_flake8()
    
    issues = parse_flake8_output(flake8_output)
    fix_issues(issues)
    print("Auto8 has completed fixing the issues.")

if __name__ == '__main__':
    main()