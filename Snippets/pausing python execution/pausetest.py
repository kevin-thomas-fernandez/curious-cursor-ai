try:   
    width = open("width.txt", "r")
    input("Press Enter to exit...")
except FileNotFoundError:
    print("Invalid input. Please enter valid input file.")
    input("Press Enter to exit...")


