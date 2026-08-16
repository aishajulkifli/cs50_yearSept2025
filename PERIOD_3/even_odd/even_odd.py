number = input("Enter a number: ")      # Get user input

if int(number) % 2 == 0:                 # Check if the number is even
    print(f"{number} is an even number.")   # Print the result
else:
    print(f"{number} is an odd number.")    # Print the result if the number is odd
