#1242 Template for console input
#R1.0 Jan 15 2025

#import random
#import string

def foo(strin):
    return str(strin).capitalize()

if __name__ == "__main__":
    while True:
        defin = 'the default string'
        inval = input(f"Please enter something: [{defin}] : ").strip() or defin
        if inval == 'exit':
            break
        print (f"You entered {inval}.")
        print (foo(inval))
