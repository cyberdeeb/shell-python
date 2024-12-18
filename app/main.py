
import os
import sys

def echo(args):
    """Handles the 'echo' command."""
    print(' '.join(args))

def type_cmd(args):
    """Handles the 'type' command."""

    paths = os.getenv("PATH").split(":")

    if (args and args[0] in commands) or args[0] == 'exit':
        print(f'{args[0]} is a shell builtin')
    else:
        for path in paths:
            if os.path.exists(f'{path}/{args[0]}'):
                print(f'{args[0]} is {path}/{args[0]}')
        else:
            print(f"{' '.join(args)}: not found")



# Command registry
commands = {'echo': echo, 
            'type': type_cmd
            }
    
def run(user_input):
    """Parses and executes the appropriate command."""
    parts = user_input.strip().split()
    # Ignore empty input
    if not parts:
        return  

    cmd, *args = parts

    if cmd == 'exit' and args == ['0']:
        sys.exit()

    cmd_run = commands.get(cmd)

    if cmd_run:
        cmd_run(args)
    else:
        print(f'{cmd}: command not found')

def main():
    """Main loop for command-line interaction."""
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        run(command)

if __name__ == "__main__":
    main()
