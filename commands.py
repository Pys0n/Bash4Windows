import os, sys, platform

from style import ANSI

history = []


def cat(user_input: list[str]) -> str:
    options = {'-A': False, '-b': False, '-e': False, '-E': False, '-n': False, '-s': False, '-t': False, '-T': False, '-v': False, '-u': False}

    for i, option in enumerate(user_input[1:]):
        if not option.startswith('-'):
            break

        if option in ('-A', '--show-all'):
            options['-v'] = True
            options['-E'] = True
            options['-T'] = True
        elif option in ('-b', '--number-nonblank'):
            options['-b'] = True
            options['-n'] = False
        elif option == '-e':
            options['-v'] = True
            options['-E'] = True
        elif option in ('-E', '--show-ends'):
            options['-E'] = True
        elif option in ('-n', '--number'):
            options['-n'] = True
        elif option in ('-s', '--squeeze-blank'):
            options['-s'] = True
        elif option == '-t':
            options['-v'] = True
            options['-T'] = True
        elif option in ('-T', '--show-tabs'):
            options['-T'] = True
        elif option in ('-v', '--show-nonprinting'):
            options['-v'] = True
        elif option in ('-h', '--help'):
            print('Concatenate FILE(s), or standard input, to standard output\nWith no FILE, or when FILE is -, read standard input.\n')
            print(f'{ANSI.BOLD + ANSI.UNDERLINE}Usage:{ANSI.END} cat [OPTION]... [FILE]...')

            option_print(
                [
                    ('-A, --show-all', 'equivalent to -vET'),
                    ('-b, --number-nonblank', 'number nonempty output lines, overrides -n'),
                    ('-e', 'equivalent to -vE'),
                    ('-E, --show-ends', 'display $ at end of each line'),
                    ('-n, --number', 'number all output lines'),
                    ('-s, --squeeze-blank', 'suppress repeated empty output lines'),
                    ('-t', 'equivalent to -vT'),
                    ('-T, --show-tabs', 'display TAB characters at ^I'),
                    ('-v, --show-nonprinting', 'use ^ and M- notation, except for LF (\\n) and TAB (\\t)'),
                    ('-u', '(ignored)'),
                    ('-h, --help', 'Print help'),
                    ('-V, --version', 'Print version'),
                ]
            )
            return
        elif option in ('-V', '--version'):
            print('cat (uutils coreutils) 0.10.0')
            return

    output = ''
    errors = ''
    if len(user_input[i+1:]) == 0:
        while True:
            try:
                output += input() + '\n'
            except EOFError:
                break
    for file in user_input[i+1:]:
        if file == '-':
            while True:
                try:
                    output += input() + '\n'
                except EOFError:
                    break
        elif os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                output += f.read()
        else:
            errors += f'cat: {file}: No such file or directory\n'
    
    if options['-s']:
        while '\n\n\n' in output:
            output = output.replace('\n\n\n', '\n\n')
    if options['-b'] or options['-n']:
        output = output.split('\n')
        number = 1
        for i, line in enumerate(output):
            if options['-b'] and line == '':
                continue
                
            output[i] = f'{str(number).rjust(6)}  {line}'
            number += 1

        output = '\n'.join(output)
    if options['-E']:
        output = output.replace('\n', '$\n')
    if options['-T']:
        output = output.replace('\t', '^I')

    return output + errors


def cd(user_input: str) -> str | None:
    path = user_input[-1]
    if os.path.exists(path):
        os.chdir(path)
    else:
        return f'cd: {path}: file or directory not found'


def clear(_: str) -> None:
    if os.name != 'nt':
        os.system('clear')
    else:
        os.system('cls')


def history_(_: str) -> str:
    output = ''
    for i, command in enumerate(history[-1000:]):
        output += f' {str(max(len(history)-999, 1)+i).rjust(4)}  {command}\n'
    
    return output.rstrip()


def pwd(_: str) -> str:
    return os.getcwd()


commands = {
    'cat': cat,
    'cd': cd,
    'clear': clear,
    'history': history_,
    'pwd': pwd,
}


def option_print(options: tuple[tuple[str]]) -> None:
    max_length = max(len(option[0]) for option in options)

    result = f'{ANSI.BOLD + ANSI.UNDERLINE}Options:{ANSI.END}'
    for option in options:
        result += f'  {ANSI.BOLD}{option[0].rjust(max_length)}{ANSI.END}  {option[1]}'
    
    print(result)