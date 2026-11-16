import os, sys, platform

from tools import *


def run() -> None:
    pwd = os.getcwd()
    user = os.getlogin()
    device = platform.node()

    while True:
        try:
            user_input = input(format_prompt(user, device, pwd)).strip()
            if user_input == 'exit':
                print('exit')
                break

            output = process_command(user_input)
            if output != None:
                print(output)
        except KeyboardInterrupt:
            print()
        except EOFError:
            print('\nexit')
            break

if __name__ == '__main__':
    run()