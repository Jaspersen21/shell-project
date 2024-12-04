import sys


def main():
    while True: # infinite loop to keep  the shell running 
        sys.stdout.write("$ ") #writing the prompt 
        sys.stdout.flush()  # ensuring the prompt is displayed immidiately

        command  = input().strip() 

        if not  command :
            continue 

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
