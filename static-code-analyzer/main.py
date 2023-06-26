import os
import re
import argparse
import ast

total_blank_lines = 0
found_blank_lines = False
message_extra = {}


def get_issue_message(code):
    message = issues_messages[code]
    for key in message_extra:
        message = message.replace("{%s}" % key, message_extra[key])
    return message


def get_issue_output(path, line_number, code):
    return f"{path}: Line {line_number}: {code} {get_issue_message(code)}"


def validate_length(line=''):
    return len(line) <= 79


def validate_indentation(line=''):
    if len(line) == 0:
        return True
    
    indents = 0
    i = 0
    while line[i] == ' ':
        indents += 1
        i += 1
    
    return indents % 4 == 0


def validate_semicolon(line=''):
    line = re.sub('#.*', '', line)
    return not line.strip().endswith(';') or line.strip().startswith('#')


def validate_spaces_before_inline_comments(line=''):
    comments = re.findall('#.*', line)
    if len(comments) != 0:
        for comment in comments:
            index = line.index(comment)
            if index >= 2 and (line[index - 1] != ' ' or line[index - 2] != ' '):
                return False
    
    return True


def validate_todo(line=''):
    comments = re.findall('#.*', line)
    for comment in comments:
        parts = comment.strip().split(' ')
        if len(parts) > 1 and parts[1].lower() == 'todo':
            return False
    
    return True


def validate_blank_lines(line=''):
    global total_blank_lines, found_blank_lines
    
    if line.strip() == '':
        total_blank_lines += 1
        if total_blank_lines == 3:
            found_blank_lines = True
    else:
        if found_blank_lines:
            reset()
            return False
        else:
            reset()
    
    return True


def validate_spaces_after_class(line=''):
    global message_extra
    
    line = line.lstrip()
    if line.startswith('class'):
        message_extra = {"name": 'class'}
        return line[6] != ' '
    
    if line.startswith('def'):
        message_extra = {"name": 'def'}
        return line[4] != ' '
    
    return True


def validate_camel_case_class(line=''):
    global message_extra
    
    line = line.strip()
    if line.startswith('class'):
        line = line.replace(' ', '')
        classname = line[5:line.find('(')]
        message_extra = {"class": classname}
        if re.match('([A-Z][a-z0-9]+)+', classname) is None:
            return False
    
    return True


def validate_snake_case_function(line=''):
    global message_extra
    
    line = line.strip()
    if line.startswith('def'):
        line = line.replace(' ', '')
        function_name = line[3:line.index('(')]
        if not function_name.startswith("__") and not function_name.endswith("__"):
            message_extra = {"function": function_name}
            if re.match('[a-z_]+(_[a-zA-Z]+)*', function_name) is None:
                return False
    
    return True


def validate_snake_case_argument(line=''):
    global message_extra
    
    line = line.strip()
    
    if line.startswith('def') or line.startswith('class'):
        params = line[line.find('(') + 1:line.find(')')].split(',')
        for param in params:
            param = param.strip()
            if param == 'self' or param == '':
                continue
            param_name = param.split('=')[0]
            if re.match('[a-z_]+(_[a-zA-Z]+)*', param_name) is None:
                message_extra['name'] = param_name
                return False
    
    return True


def validate_mutable_argument(line=''):
    global message_extra
    
    line = line.strip()
    
    if line.startswith('def'):
        params = line[line.find('(') + 1:line.find(')')].split(',')
        for param in params:
            param = param.strip()
            if param == 'self':
                continue
            param_parts = param.split('=')
            if len(param_parts) > 1:
                param_default_value = param_parts[1]
                param_default_value_type = type(ast.literal_eval(param_default_value))
                if type([]) == param_default_value_type:
                    return False
    
    return True


def validate_snake_case_variable(line=''):
    global message_extra
    
    line = line.strip()
    
    if not line.startswith('def') and not line.startswith('class') and line != '':
        parts = line.split('=')
        if len(parts) > 1:
            variable_name = parts[0].strip()
            if not variable_name.startswith('self.'):
                if re.match('[a-z_]+(_[a-zA-Z]+)*', variable_name) is None:
                    message_extra['name'] = variable_name
                    return False
    
    return True


def reset():
    global total_blank_lines, found_blank_lines, message_extra
    
    total_blank_lines = 0
    found_blank_lines = False
    message_extra = {}


def analyze_file(filename=''):
    code_issues = []
    reset()
    if os.access(filename, os.F_OK):
        with open(filename, 'r') as file:
            lines = file.readlines()
    else:
        return
    
    for i in range(len(lines)):
        line = lines[i]
        for code in issues_messages:
            if not issues_validators[code](line):
                code_issues.append(get_issue_output(filename, i + 1, code))
    
    for issue in code_issues:
        print(issue)


issues_messages = {
    "S001": "Too Long",
    "S002": "Indentation is not a multiple of four",
    "S003": "Unnecessary semicolon",
    "S004": "At least two spaces required before inline comments",
    "S005": "TODO found",
    "S006": "More than two blank lines used before this line",
    "S007": "Too many spaces after '{name}'",
    "S008": "Class name '{class}' should use CamelCase",
    "S009": "Function name '{function}' should use snake_case",
    "S010": "Argument name '{name}' should be snake_case",
    "S011": "Variable '{name}' in function should be snake_case",
    "S012": "Default argument value is mutable",
}

issues_validators = {
    "S001": validate_length,
    "S002": validate_indentation,
    "S003": validate_semicolon,
    "S004": validate_spaces_before_inline_comments,
    "S005": validate_todo,
    "S006": validate_blank_lines,
    "S007": validate_spaces_after_class,
    "S008": validate_camel_case_class,
    "S009": validate_snake_case_function,
    "S010": validate_snake_case_argument,
    "S011": validate_snake_case_variable,
    "S012": validate_mutable_argument,
}

parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()

if os.access(args.path, os.F_OK):
    if os.path.isfile(args.path):
        analyze_file(args.path)
    elif os.path.isdir(args.path):
        for filename in os.listdir(args.path):
            filepath = os.path.join(args.path, filename)
            if os.path.isfile(filepath) and re.match(r'.+_\d+.py$', filename):
                analyze_file(filepath)
