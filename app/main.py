import sys

BUILTINS = {"echo", "exit", "type"}

def main():
    while True: # infinite loop to keep  the shell running 
        sys.stdout.write("$ ") #writing the prompt 
        sys.stdout.flush()  # ensuring the prompt is displayed immidiately

        command  = input().strip() 

        if not  command :
            continue 

        if command.startswith("exit"):
            # Split the command to check for an exit code
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():  # Ensure the exit code is a number
                sys.exit(int(parts[1]))  # Exit with the specified code
            elif len(parts) == 1:
                sys.exit(0)  # Default exit code is 0
            else:
                print(f"{command}: invalid syntax")
                continue 

        if command.startswith("echo"):
            # Remove the "echo" part and print the rest of the command
            print(command[5:].strip())  # Slice after "echo " and strip extra spaces
            continue  

        if command.startswith("type"):
             parts = command.split(maxsplit=1)  # Split into "type" and the argument
             if len(parts) == 2:
                cmd_to_check = parts[1]
                if cmd_to_check in BUILTINS:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    print(f"{cmd_to_check}: not found")
             else:
                print("type: usage: type <command>")
             continue  

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
