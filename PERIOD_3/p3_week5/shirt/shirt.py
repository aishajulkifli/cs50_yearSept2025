import sys
import os                           # os is used for handling file paths and extensions
from PIL import Image, ImageOps     # PIL = Python Imaging Library, Pillow is a fork of PIL

def main():
    # Check number of arguments
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    valid_ext = [".jpg", ".jpeg", ".png"]

    input_file = sys.argv[1]        # Get input file from command-line argument, 1 is the first argument after the script name
    output_file = sys.argv[2]       # Get output file from command-line argument, 2 is the second argument after the script name

    # Get file extensions
    input_ext = os.path.splitext(input_file)[1].lower()     # os.path.splitext splits the file name into a tuple (root, ext), we take the second element [1] which is the extension, and convert it to lowercase for comparison
    output_ext = os.path.splitext(output_file)[1].lower()   # Same as above for output file

    # Validate extensions
    if input_ext not in valid_ext:
        sys.exit("Invalid input")       # .exit() is used to exit the program with a message, it will print the message and then terminate the program
    if output_ext not in valid_ext:
        sys.exit("Invalid output")
    if input_ext != output_ext:
        sys.exit("Input and output have different extensions")

    try:
        # Open input image
        image = Image.open(input_file)
    except FileNotFoundError:
        sys.exit("Input does not exist")

    # Open shirt image
    shirt = Image.open("shirt.png")

    # Resize and crop input image to match shirt size
    size = shirt.size
    image = ImageOps.fit(image, size)

    # Overlay shirt on top
    image.paste(shirt, shirt)

    # Save output image
    image.save(output_file)


if __name__ == "__main__":
    main()

# python shirt.py before1.jpg after1.jpg
