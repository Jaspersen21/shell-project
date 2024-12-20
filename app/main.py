import sys
import os
import subprocess
import shlex  # For parsing quoted strings

# List of supported shell built-ins
BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def find_executable(command):
    """
    Search for an executable in the directories listed in PATH.
    Returns the full path if found, otherwise None.
    """
    path_dirs = os.environ.get("PATH", "").split(":")  # Get PATH and split into directories
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):  # Check if it's executable
            return full_path
    return None

def parse_command(command_line):
    """
    Parse the command line input, handling single quotes properly.
    """
    try:
        return shlex.split(command_line, posix=True)  # shlex handles quoted strings
    except ValueError as e:
        print(f"Error parsing command: {e}")
        return []

def main():
    while True:  # Continuous loop to keep the shell running
        # Display the shell prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()  # Ensure the prompt is displayed immediately

        # Read user input
        command_line = input().strip()  # Remove leading/trailing whitespace

        # Skip empty input
        if not command_line:
            continue

        # Parse the command and its arguments
        parts = parse_command(command_line)
        if not parts:
            continue
        command = parts[0]  # First part is the command
        args = parts[1:]    # Remaining parts are arguments

        # Handle the exit command
        if command == "exit":
            if len(args) == 1 and args[0].isdigit():  # Exit with a specific code
                sys.exit(int(args[0]))
            elif len(args) == 0:  # Exit with default code 0
                sys.exit(0)
            else:
                print(f"{command_line}: invalid syntax")
                continue

        # Handle the echo command
        if command == "echo":
            print(" ".join(args))  # Join the arguments with spaces and print
            continue

        # Handle the pwd command
        if command == "pwd":
            print(os.getcwd())  # Print the current working directory
            continue

        # Handle the cd command
        if command == "cd":
            if len(args) == 1:  # Ensure exactly one argument
                path = args[0]
                if path == "~":  # Handle the ~ character for the home directory
                    home_dir = os.environ.get("HOME")
                    if home_dir:
                        path = home_dir
                    else:
                        print("cd: HOME environment variable is not set")
                        continue
                try:
                    os.chdir(path)  # Change the current working directory
                except FileNotFoundError:
                    print(f"cd: {path}: No such file or directory")
                except NotADirectoryError:
                    print(f"cd: {path}: Not a directory")
                except PermissionError:
                    print(f"cd: {path}: Permission denied")
            else:
                print("cd: usage: cd <directory>")
            continue

        # Handle the type command
        if command == "type":
            if len(args) == 1:
                cmd_to_check = args[0]
                if cmd_to_check in BUILTINS:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    executable_path = find_executable(cmd_to_check)
                    if executable_path:
                        print(f"{cmd_to_check} is {executable_path}")
                    else:
                        print(f"{cmd_to_check}: not found")
            else:
                print("type: usage: type <command>")
            continue

        # Handle external programs
        executable_path = find_executable(command)
        if executable_path:
            try:
                # Run the external program with arguments
                result = subprocess.run([executable_path] + args, text=True, capture_output=True)
                print(result.stdout, end="")  # Print the program's standard output
                if result.stderr:  # Print standard error if any
                    print(result.stderr, file=sys.stderr, end="")
            except Exception as e:
                print(f"Error running {command}: {e}")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
