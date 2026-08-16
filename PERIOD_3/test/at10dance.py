from machine import Pin, PWM, SPI
from mrfc522 import MFRC522
import time

# Pin Definitions
sck_pin, mosi_pin, miso_pin = 14, 15, 12
sda_pin, rst_pin = 2, 17
led_green = Pin(11,Pin.OUT)
led_red = Pin(10,Pin.OUT)

# Buzzer Setup using PWM on Pin 18
buzzer = PWM(Pin(18))

# Initialize Reader
reader = MFRC522(sck_pin, mosi_pin, miso_pin, rst_pin, sda_pin)

# Access List
allowed_users = {
    "0x71-0xa7-0x2f-0xaa-0x53": "Aisha",
    "0xd3-0x50-0x15-0x14-0x82": "Vyshna",
}

def play_beep(freq, duration_ms):
    buzzer.freq(freq)      # Set pitch (e.g., 1000 for a high beep)
    buzzer.duty_u16(30000) # Turn volume on (approx 50% duty cycle)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)     # Turn off

print("Reader initialized! Place a tag...")

while True:
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        (stat, uid) = reader.anticoll()
        if stat == reader.OK:
            uid_str = "-".join([hex(i) for i in uid])
            print("---------------------------")
            print("UID Detected:", uid_str)

            if uid_str in allowed_users:
                print("Access Granted:", allowed_users[uid_str])
                led_green.value(1)
                play_beep(2000, 200) # Short high beep for Success
                time.sleep_ms(100)
                led_green.value(0)
            else:
                print("Access Denied!")
                # Double low beep for Error
                led_red.value(1)
                play_beep(400, 500)
                time.sleep_ms(100)
                play_beep(400, 500)
                led_red.value(0)

            time.sleep(1) # Prevent multiple reads of the same card

    time.sleep(0.1)
