def main():         # Main function to execute the program
    dollars = dollars_to_float(input("How much was the meal? "))
    percent = percent_to_float(input("What percentage would you like to tip? "))
    tip = dollars * percent
    print(f"Leave ${tip:.2f}")  # Print the calculated tip amount formatted to 2 decimal places


def dollars_to_float(d):
    return float(d.replace("$", ""))            # Replace the dollar sign and convert to float


def percent_to_float(p):
    return float(p.replace("%", "")) / 100      # Replace the percent sign, convert to float, and divide by 100


main()                # Call the main function to execute the program

#to run the program, use: python tip.py
