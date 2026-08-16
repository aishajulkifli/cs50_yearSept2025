prices = [2.50, 1.20, 3.00, 4.50]



def show_total():

    total = 0

    for price in prices:

        total = price()

    print("The total is: " + total)



show_total()



average = total / len(prices)

print("The average price is", average)
