from cs50 import get_float

change = 0                                       # variable to store the amount of change the user enters
coins = 0                                        # to keep track of the total number of coins used

while change <= 0:                               # Prompt user for change (in dollars)
    change = get_float("Change: ")

def remain(coin_value):                          # Function to count how many coins of a given value can be used
    global change                                # call the change function
    global coins
    while (change >= coin_value):
        change = round(change - coin_value, 10)  # subtract coin and round to avoid floating errors
        coins += 1                               # count each coin used


# Try each coin type
remain(0.25)    # quarters
remain(0.10)    # dimes
remain(0.05)    # nickels
remain(0.01)    # pennies

# Print total coins used
print(coins)
