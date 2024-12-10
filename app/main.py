import sys

def echo(args):
    """Handles the 'echo' command."""
    print(' '.join(args))

def type_cmd(args):
    """Handles the 'type' command."""

    if args and args[0] in commands:
        print(f'type {args[0]} is a shell builtin')
    else:
        print(f"{' '.join(args)}: command not found")

# Command registry
commands = {'echo': echo, 
            'type': type_cmd
            }
    
def run(user_input):
    """Parses and executes the appropriate command."""
    parts = user_input.strip().split()
    if not parts:
        return  # Ignore empty input

    cmd, *args = parts

    if cmd == 'exit' and args == ['0']:
        sys.exit()

    cmd_run = commands.get(cmd)

    if cmd_run:
        cmd_run(args)
    else:
        print(f'{cmd}: command not found')

def main():

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        run(command)

if __name__ == "__main__":
    main()
