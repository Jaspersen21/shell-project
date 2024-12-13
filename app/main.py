import sys
import os
import subprocess

def find_executable(command):

    path_dirs = os.environ.get("PATH", "").split(":")  # check file and change them to directories 
    for  directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):  # Check if it's executable
            return full_path
    return None

BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def main():
    while True: # infinite loop to keep  the shell running 
        sys.stdout.write("$ ") #writing the prompt 
        sys.stdout.flush()  # ensuring the prompt is displayed immidiately

        command_line  = input().strip() 

        if not  command_line :
            continue 

        parts = command_line.split()
        command = parts[0] #  firstpart ofthe  command line
        args   = parts[1:] # remaining part is arguments


        if command == "exit":
            if len(args) == 1 and args[0].isdigit():  # Exit with a specific code
                sys.exit(int(args[0]))
            elif len(args) == 0:  # Exit with default code 0
                sys.exit(0)
            else:
                print(f"{command_line}: invalid syntax")
                continue

        if command == "echo":
            print(" ".join(args))  # Join the arguments with spaces and print
            continue

        if command == 'pwd':
            print(os.getcwd())  # Print the current working directory
            continue

        if command == "cd":
            if len(args) == 1:  # Ensure exactly one argument
                path = args[0]
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
