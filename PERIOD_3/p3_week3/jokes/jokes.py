import sys          # sys is a short for system.
import pyjokes

LANGUAGES = ["cs", "de", "en", "es", "eu", "fr", "gl", "hu", "it", "lt", "pl", "ru", "sv"]

def read_arg():
    default = "en"

    # No argument given
    if len(sys.argv) < 2:       # sys.argv is a list in Python that contains the command-line arguments passed to the script. The first element (sys.argv[0]) is the name of the script itself, and any additional elements are the arguments provided by the user. If len(sys.argv) < 2, it means that no additional arguments were given, and the function will
        return default

    # Only first extra argument is handled
    arg = sys.argv[1]

    # Must start with "-" and be exactly 3 characters (-fr)
    if not arg.startswith("-") or len(arg) != 3:
        return default

    # Convert to lowercase
    lang = arg[1:].lower()      # [1:] slices the string to get the part after the first character, which is the language code (e.g., "fr" from "-fr"). The .lower() method converts the language code to lowercase to ensure case-insensitive comparison.

    # Check if language exists
    if lang in LANGUAGES:
        return lang
    else:
        return default

# Get a single joke in the specified language
def get_single_joke(lang):
    try:
        if lang not in LANGUAGES:
            return "Bad joke"
        joke = pyjokes.get_joke(language=lang)
        return joke
    except Exception:           # Catch any exception that may occur during the joke retrieval process and return "Bad joke" if an error occurs (e.g., if the language is not supported or if there is an issue with the pyjokes library).
        return "Bad joke"       # The "Bad joke" string is returned as a fallback in case of any errors, ensuring that the program does not crash and provides a response even when something goes wrong.

# Main function to read the language argument and print a joke
def main():
    lang = read_arg()
    joke = get_single_joke(lang)
    print(joke)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

# pytest test_jokes.py
# run with: pytest test_jokes.py
