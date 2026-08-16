def main():
    plate = input("Plate: ")        # Get user input for the license plate
    if is_valid(plate):             #is_valid function checks if the plate is valid according to the rules
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):                    # Function to check if the license plate is valid

    if len(s) < 2 or len(s) > 6:    # Length must be between 2 and 6
        return False

    if not s[0:2].isalpha():        # First two characters must be letters
        return False

    if not s.isalnum():             # Only letters and numbers allowed
        return False

    number_started = False          # Numbers must be at the end and cannot start with 0

    for char in s:
        if char.isdigit():          # If the character is a digit, check if the number has started
            if not number_started:  # If the number has not started, set number_started to True
                number_started = True
                if char == "0":     # If the first number is 0, return False
                    return False
        else:
            if number_started:
                return False

    return True


main()      # Call the main function to execute the program
