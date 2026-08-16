from machine import Pin, ADC    # Pin for controlling segments and digits, ADC for reading voltage
import utime                    # for timing and delays

# volt divider resistors
R1 = 47000
R2 = 22000

#----SEGMENT PINS----
segA = Pin(21, Pin.OUT)         # segment A is connected to GPIO21, set as output, to control the turn on/off of the segment
segB = Pin(20, Pin.OUT)
segC = Pin(19, Pin.OUT)
segD = Pin(18, Pin.OUT)
segE = Pin(17, Pin.OUT)
segF = Pin(16, Pin.OUT)
segG = Pin(14, Pin.OUT)
segDP = Pin(15, Pin.OUT)

segments = [segA, segB, segC, segD, segE, segF, segG, segDP]    # list of all segment pins for easy control

#----DIGIT PINS----
digit2 = Pin(10, Pin.OUT)       #
digit3 = Pin(11, Pin.OUT)
digit4 = Pin(12, Pin.OUT)

digits = [digit2, digit3, digit4]

#----ADC SETUP----
adc = ADC(0) #GP26 is ADC0, connected to the voltage divider output

#----SEGMENT PATTERNS FOR 0-9 + L ----
numbers = {
    0: [1,1,1,1,1,1,0,0],
    1: [0,1,1,0,0,0,0,0],
    2: [1,1,0,1,1,0,1,0],
    3: [1,1,1,1,0,0,1,0],
    4: [0,1,1,0,0,1,1,0],
    5: [1,0,1,1,0,1,1,0],
    6: [1,0,1,1,1,1,1,0],
    7: [1,1,1,0,0,0,0,0],
    8: [1,1,1,1,1,1,1,0],
    9: [1,1,1,1,0,1,1,0],
    "L":[0,0,0,1,1,1,0,0] # segments D, E, F
}

# ---- MAIN LOOP ----
def main():
    while True:
        v = read_voltage()      # v is the voltage read from the ADC, converted to the input voltage using the voltage divider formula
        display_number(v)

#----Function to display one digit----
def show_digit(value, digit_pin, show_dp=False):  # sho

    # turn all digits off
    for d in digits:
        d.value(0)

    # turn all segments off
    for seg in segments:
        seg.value(0)

    #load the pattern
    pattern = numbers[value]

    # Set segment
    for i in range(7): #A-G
        segments[i].value(pattern[i])

    # Decimal Point
    if show_dp:
        segDP.value(1)
    else:
        segDP.value(0)

    digit_pin.value(1) # turn this one on
    utime.sleep_ms(1)  # small delay for multiplexing

# ---- FUNCTION TO DISPLAY A FULL 3-DIGIT NUMBER ----
def display_number(value):

    # OVER LIMIT CHECK
    if value > 9.99:
        # show O on digit 2
        show_digit(0, digit2, show_dp=False)

        # show L on digit 3
        show_digit("L", digit3, show_dp=False)

        # Turn off digit 4
        digit4.value(0)
        for seg in segments:
            seg.value(0)

        return

    #----Normal number display----
    # convert number to string with 2 decimals
    s = "{:.2f}".format(value)

    # extract digits
    d2 = int(s[0])
    d3 = int(s[2])
    d4 = int(s[3])

    # show digit
    show_digit(d2, digit2, show_dp=True) # Dp between digit 2 and 3
    show_digit(d3, digit3, show_dp=False)
    show_digit(d4, digit4, show_dp=False)

# ---- READ ADC AND CONVERT TO VOLTAGE ----
def read_voltage():
    # avg to reduce the noise
    samples = 100
    total = 0
    for _ in range(samples):
        total += adc.read_u16()     # read_u16() returns a value between 0 and 65535, representing the voltage at the ADC pin relative to the reference voltage (3.3V)
    raw = total / samples           # raw = average ADC value, still in the range 0-65535


    voltage = (raw / 65535) * 3.3 # convert to 0–3.3V, why 3.3? because the ADC reference voltage is 3.3V, so the raw value is scaled to this range
    v_in = ((voltage / (R2/(R2 + R1))))*2   # why *2? because the voltage divider output is half of the input voltage, so we multiply by 2 to get the original input voltage before the divider

    return v_in     # return the calculated input voltage based on the voltage divider formula

main()
