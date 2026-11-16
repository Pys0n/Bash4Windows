import os, sys, platform
if os.name != 'nt':
    import readline

from style import ANSI
from commands import commands, history

def format_prompt(user: str, device: str, pwd: str) -> str:
    return f'{ANSI.GREEN + ANSI.BOLD}{user}@{device}{ANSI.END}:{ANSI.BLUE + ANSI.BOLD}{pwd.replace(os.path.expanduser('~'), '~')}{ANSI.END}$ '


def process_command(user_input: str) -> str | None:
    history.append(user_input)

    user_input = split_command(user_input)

    if user_input[0] in commands:
        return commands[user_input[0]](user_input)
    else:
        return f'{user_input[0]}: command not found'


def split_command(user_input: str) -> list[str]:
    quote = False
    parts = []
    current = ''
    escaped = False
    for symbol in user_input:
        if quote and symbol == '\\':
            escaped = True
            current += symbol
        else:
            if not (not quote and symbol == ' '):
                current += symbol

        if not escaped and symbol in '"\'':
            if quote:
                quote = False
                parts.append(current)
                current = ''
        if not quote and symbol == ' ':
            parts.append(current)
            current = ''    

        if quote and symbol != '\\':
            escaped = False
    
    parts.append(current)
    
    return parts