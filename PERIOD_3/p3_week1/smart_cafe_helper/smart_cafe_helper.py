def welcome_message():
    message = "Welkom bij Smart Cafe!"
    fancy = "" # Initialize an empty string to build the fancy message

    for char in message:
        fancy = fancy + char + "."  # Add each character from the message followed by a dot to the fancy string

    print(fancy)

def calculate_tip():
        price = float(input("Wat is de prijs van het artikel? "))  # Prompt the user to enter the price of the item
        print(f"De prijs van het artikel is {price} €.")  # Print the price of the item

        tip_percent = float(input("Wat is het percentage van de fooi dat u wilt geven? "))  # Prompt the user to enter the tip percentage
        tip = price * (tip_percent / 100) # Calculate the tip amount based on the price and tip percentage
        total_price = price + tip  # Calculate the total price by adding the original price and the tip
        print(f"Fooi: ({tip_percent}%): €{tip}")  # Print the calculated tip amount with the percentage
        print(f"Totale prijs: €{total_price}")   # Print the total price to be paid by the customer

def calculate_mass_energy():
        mass_gram = float(input("Wat is het gewicht van het artikel in gram? ")) # Prompt the user to enter the weight of the item in kilograms
        mass = mass_gram / 1000  # Convert the weight from grams to kilograms
        c = 300000000  # Speed of light in meters per second
        energy = mass * c * c # Calculate the energy using Einstein's mass-energy equivalence formula (E=mc^2)
        print(f"De energie van het artikel is {energy} joules. ")

def smart_cafe_helper():
    welcome_message()       # Call the welcome_message function to display the welcome message and menu
    while True:
        order = input("Wat wilt u bestellen? ").lower()  # .lower() converts the input to lowercase, making it easier to compare with menu items

        if order == "koffie":
            print(f"Lekker! ☕")
        elif order == "thee":
            print(f"Smakelijk! 🍵")
        elif order == "cupcake":
            print(f"Yummy! 🧁")
        elif order == "boterham":
            print(f"Heerlijk! 🥪")
        else:
            print(f"Sorry, dat artikel staat niet op de menukaart. U kunt kiezen uit koffie, thee, cupcake of boterham. 🙁")
            continue  # Skip the rest of the loop and prompt the user to enter their order again

        calculate_tip()  # Call the calculate_tip function to calculate and display the tip and total price
        calculate_mass_energy()  # Call the calculate_mass_energy function to calculate and display the energy

        continue_order = input("Wilt u nog iets anders bestellen? (ja/nee)) ").lower()
        if continue_order == "nee":
            print(f"Bedankt voor je bestelling! Fijne dag verder! 😊")
            break

smart_cafe_helper()
