#!/usr/bin/python3
import sys

def read_pipe_input():
    data = sys.stdin.read()
    return data

def apply_sarcastic_mode(string):
    sarcastic_string = [string[x].lower() if x % 2 == 0 else string[x].upper() for x in range(len(string))]
    return "".join(sarcastic_string)

def main():
    try:
        if len(sys.argv) > 1:
            arguments = ' '.join(sys.argv[1:])
            print(apply_sarcastic_mode(arguments))
        else:
            pipe_data = read_pipe_input().strip()
            print(apply_sarcastic_mode(pipe_data))
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
