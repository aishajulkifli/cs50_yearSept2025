def main():
    greeting = input("Greeting: ")      # Get user input for the greeting
    print(f"${value(greeting)}")


def value(greeting):
    greeting = greeting.lower()         # Convert the greeting to lowercase for case-insensitive comparison

    if greeting.startswith("hello"):    # Check if the greeting starts with "hello"
        return 0
    elif greeting.startswith("h"):      # Check if the greeting starts with "h"
        return 20
    else:
        return 100                      # If the greeting does not start with "hello" or "h", return 100


if __name__ == "__main__":              # __name__ is a special variable in Python that is set to "__main__" when the script is run directly. This condition ensures that the main() function is only called when the script is executed directly, and not when it is imported as a module in another script.
    main()

# pytest test_twttr.py
# run with: pytest test_twttr.py
