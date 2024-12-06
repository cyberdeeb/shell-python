import sys

def echo(user_input):
    """Handles the 'echo' command."""
    print(' '.join(user_input.split(' ')[1:]))

def main():

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command == 'exit 0':
            sys.exit()
        
        if command.startswith('echo'):
            echo(command)
        else:
            print(f'{command}: command not found')


if __name__ == "__main__":
    main()
