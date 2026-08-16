import random           # Importing the random module to generate random numbers for the guessing game

print(f"Welcome to the Supermarket Survivor Game!")         # Print a welcome message to the player
print(f"You are in an abandoned supermarket and must solve puzzles to escape!")
print(f"Good luck! 💀")

while True:                             # Start an infinite loop to keep the game running until the player chooses to exit
    print("\nChoose an option:")        # Print the menu of puzzles for the player to choose from
    print("1. File Extensions: What's in this file?")
    print("2. Math Interpreter: Unlock the safe")
    print("3. Nutrition Facts: Prepare a meal")
    print("4. CamelCase Decoder: Decode the message")
    print("5. Emojize: Guess the clue")
    print("6. Guessing Game: Guess the secret code")
    print("7. Exit")

    choice = input("Make a choice (1-7): ")     # Get the player's choice for the puzzle they want to solve

    if choice == "1":
        filename = input("Type the name of the file to check its extension: ")

        if filename.endswith(".pdf"):
            print("This is a PDF file containing a recipe!")
        elif filename.endswith(".txt"):
            print("This is a text file.")
        elif filename.endswith(".exe"):
            print("Warning! This is an executable file!")
        else:
            print("Unknown file type!")

    elif choice == "2":
        expression = input("Enter the mathematical expression (e.g., 2 + 3 * 4 + 5): ")     # Get a mathematical expression from the player to evaluate and unlock the safe

        try:
            result = eval(expression)       # expression is evaluated using the eval() function, which takes a string and evaluates it as a Python expression.
            print("The result is:", result)
            print("The safe opens!")
        except:
            print("Invalid expression! Try again.")

    elif choice == "3":
        calories = 0
        food_calories = {
            "apple": 95,
            "banana": 105,
            "cookie": 150,
            "sandwich": 250,
            "water": 0
        }

        print("You need 500 calories to proceed.")

        while calories < 500:
            food = input("Choose an item (apple, banana, cookie, sandwich, water): ")

            if food in food_calories:
                calories += food_calories[food]         # += is used to add the calories of the chosen food item to the total calories
                print(f"{food} added! Total calories:", calories)
            else:
                print("Invalid food choice.")

        print("Congratulations! You have enough energy.")

    elif choice == "4":
        message = input("Type the CamelCase message to decode: ")

        decoded = ""        # Initialize an empty string to build the decoded message
        for letter in message:
            if letter.isupper():
                decoded += " " + letter     # If the letter is uppercase, add a space before it and then add the letter to the decoded string
            else:
                decoded += letter

        print("Decoded message:", decoded.strip())

    elif choice == "5":                     # Provide a clue in emojis and ask the player to guess what they mean
        print("You find a clue in emojis: 🍕 🍬 🍉")
        answer = input("What do these emojis mean? ")

        if answer.lower() == "pizza candy watermelon":
            print("Correct! You receive a key.")
        else:
            print("That's not correct. Try again!")

    elif choice == "6":
        secret = random.randint(1, 10)      # Generate a random secret code between 1 and 10 for the guessing game using the import random module
        attempts = 3

        while attempts > 0:
            guess = int(input(f"Guess the code (attempts left: {attempts}): "))

            if guess < secret:
                print("Too low!")
            elif guess > secret:
                print("Too high!")
            else:
                print("Correct! The door opens.")
                break

            attempts -= 1

        if attempts == 0:
            print("Unfortunately! The code was", secret)

    elif choice == "7":
        print("Thank you for playing! See you next time.")
        break           # Exit the game loop and end the program when the player chooses to exit
