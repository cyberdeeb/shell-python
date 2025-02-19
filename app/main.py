
import os
import subprocess
import sys
import shlex

def cd(args):
    """Handles the 'cd' command."""

    directory = args[0]

    # Handles cd to home directory
    if directory == '~':
        home = os.path.expanduser('~')
        os.chdir(home)
    # Handles input directory change
    elif os.path.isdir(directory):
        os.chdir(directory)
    else:
        print(f'cd: {directory}: No such file or directory')


def echo(args):
    """Handles the 'echo' command."""
    print(' '.join(args))

def pwd(args):
    """Handles the 'pwd' command."""
    print(os.getcwd())

def type_cmd(args):
    """Handles the 'type' command."""

    paths = os.getenv("PATH").split(":")

    if (args and args[0] in commands) or args[0] == 'exit':
        print(f'{args[0]} is a shell builtin')
    else:
        # Search for program path in PATH
        for path in paths:
            if os.path.exists(f'{path}/{args[0]}'):
                print(f'{args[0]} is {path}/{args[0]}')
                break
        # Executed if loop completes and no match
        else:
            print(f"{' '.join(args)}: not found")

def execute(args):
    """Handles program execution and not found errors"""
    paths = os.getenv("PATH").split(":")

    for path in paths:
        potential_path = f'{path}/{args[0]}'
        if os.path.exists(potential_path):
            program_path = potential_path
            break
    else:  # This runs only if the loop did NOT encounter a break
        print(f"{' '.join(args)}: command not found")
        return  # Exit the function if the program was not found
    
    if program_path is None:  # If the program was not found
        print(f"{' '.join(args)}: not found")
        return  # Exit if not found
    
    # Extract the basename of the program
    program_basename = os.path.basename(program_path)
    
    
    try:
        # Run the program with its arguments
        subprocess.run([program_basename] + args[1:], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {program_path}: {e}")
    except FileNotFoundError:
        print(f"Program not found: {program_path}")

# Command registry
commands = {'cd' : cd,
            'echo': echo, 
            'pwd': pwd,
            'type': type_cmd
            }
    
def run(user_input):
    """Parses and executes the appropriate command with support for output redirection."""
    try:
        parts = shlex.split(user_input)
    except ValueError as e:
        print(f'Error parsing input: {e}')
        return
    
    if not parts:
        return  # Ignore empty input

    # Handle redirection (>)
    if ">" in parts or "1>" in parts:
        try:
            redir_index = parts.index(">") if ">" in parts else parts.index("1>")
            command_part = parts[:redir_index]  # Command before ">"
            output_file = parts[redir_index + 1]  # File after ">"
        except IndexError:
            print("Syntax error: No output file specified")
            return

        # Ensure the parent directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Create missing directories

        # Open file for writing and redirect stdout
        with open(output_file, "w") as f:
            result = subprocess.run(command_part, stdout=f, stderr=subprocess.PIPE, text=True)
            
            # If there's an error, print it to stderr
            if result.returncode != 0:
                sys.stderr.write(result.stderr)
                sys.stderr.flush()
        return
    
    # Normal execution if no redirection
    cmd, *args = parts

    if cmd == 'exit' and args == ['0']:
        sys.exit()

    cmd_run = commands.get(cmd)

    if cmd_run:
        cmd_run(args)
    else:
        execute([cmd] + args)



def main():
    """Main loop for command-line interaction."""
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        run(command)

if __name__ == "__main__":
    main()
