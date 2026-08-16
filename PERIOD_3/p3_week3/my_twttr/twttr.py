def main():
    word = input("Input: ")             # Prompt the user for input
    print("Output:", shorten(word))     # Print the output of the shorten function


def shorten(word):
    vowels = "AEIOUaeiou"       # Define a string of vowels (both uppercase and lowercase)
    result = ""                 # Initialize an empty string to store the result

    for letter in word:
        if letter not in vowels:    # If the letter is not a vowel, add it to the result
            result += letter        # += is a shorthand for result = result + letter

    return result


if __name__ == "__main__":
    main()

# pytest test_twttr.py
# run with: pytest test_twttr.py
