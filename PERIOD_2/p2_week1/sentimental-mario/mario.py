
height = 0                                              # start height w 0 value

while height < 1 or height > 8:                         # to set a valid value
    height = int(input("Height:"))                      # promt input from user, interger

for i in range(height):
    print(" " * (height - 1 - i), end = "")             # printing the spaces - 1 for the given value
    print("#" * (i + 1))                                # print # + 1 from previous value
