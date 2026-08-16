def main():
    plate = input("Plate: ")        # Prompt the user for a vanity plate
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):               # Check if the vanity plate is valid according to the specified rules
    if len(s) < 2 or len(s) > 6:    # Length must be between 2 and 6 characters
        return False

    if not s[0:2].isalpha():        # Must start with at least two letters
        return False

    if not s.isalnum():             # Must contain only letters and numbers
        return False

    number_started = False

    for i, char in enumerate(s):    # enumerate to check each character and its position
        if char.isdigit():
            if not number_started:
                if char == "0":     # First number cannot be 0
                    return False
                number_started = True
        else:
            if number_started:
                return False

    return True


if __name__ == "__main__":
    main()

# pytest test_plates.py
# run with: pytest test_plates.py
