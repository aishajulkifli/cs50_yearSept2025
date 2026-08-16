def main():
    fraction = input("Fraction: ")      # Prompt the user to input a fraction, e.g., "1/2"
    percentage = convert(fraction)      # Convert the fraction to a percentage using the convert function
    print(gauge(percentage))            # Print the fuel gauge reading based on the percentage using the gauge function


def convert(fraction):
    try:
        x, y = fraction.split("/")      # Split the input string into numerator (top nmbr) and denominator (bottom nmbr) using the "/" as a delimiter
        x = int(x)
        y = int(y)
    except ValueError:
        raise ValueError

    if y == 0:
        raise ZeroDivisionError         # Raise an error if the denominator is zero to prevent division by zero

    if x > y:
        raise ValueError

    percentage = round((x / y) * 100)
    return percentage


def gauge(percentage):
    if percentage <= 1:     # If the percentage is 1% or less, return "E" for empty
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()

# pytest test_fuel.py
# run with: pytest test_fuel.py
