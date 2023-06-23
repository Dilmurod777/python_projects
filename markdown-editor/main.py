def help_command():
    print("Available formatters: " + ' '.join(formatters))
    print('Special commands: ' + ' '.join(commands))


def done_command():
    global isDone, text
    isDone = True
    
    with open('output.md', 'w') as file:
        file.write(text.lstrip())


def header_formatter():
    while True:
        try:
            level = int(input("Level: "))
            if level < 1 or level > 6:
                print("The level should be within the range of 1 to 6")
            else:
                text = input("Text: ")
                return "\n" + "#" * level + ' ' + text + '\n'
        except ValueError:
            print("Invalid input. Try again!")


def plain_formatter():
    text = input("Text: ")
    return text


def bold_formatter():
    text = input("Text: ")
    return f"**{text}**"


def italic_formatter():
    text = input("Text: ")
    return f"*{text}*"


def inline_code_formatter():
    text = input("Text: ")
    return f"`{text}`"


def new_line_formatter():
    return '\n'


def link_formatter():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"


def list_formatter(unordered=False):
    while True:
        try:
            n = int(input("Number of rows: "))
            if n < 1:
                print('The number of rows should be greater than zero')
            else:
                els = []
                for i in range(n):
                    el = input(f"Row #{i + 1}: ")
                    if unordered:
                        el = f"- {el}"
                    else:
                        el = f"{i + 1}. {el}"
                    els.append(el)
                return '\n'.join(els) + '\n'
        except ValueError:
            print("Invalid input. Try again!")
    pass


isDone = False
formatters = {
    "header": header_formatter,
    'plain': plain_formatter,
    'bold': bold_formatter,
    'italic': italic_formatter,
    'inline-code': inline_code_formatter,
    'new-line': new_line_formatter,
    'link': link_formatter,
    'ordered-list': list_formatter,
    'unordered-list': lambda: list_formatter(True)
}
commands = {
    '!help': help_command,
    '!done': done_command
}
text = ""

while not isDone:
    choice = input("Choose a formatter: ")
    
    if choice in commands:
        commands[choice]()
    elif choice in formatters:
        text += formatters[choice]()
        print(text.lstrip())
    else:
        print('Unknown formatting type or command')
