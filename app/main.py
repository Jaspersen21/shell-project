import sys


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

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
