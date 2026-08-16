from machine import Pin, PWM, SPI, I2C          # Hardware interfaces
from mrfc522 import MRFC522                     # RFID reader library, RFID is Radio-frequency identification
import time                                     # Time library for delays and timestamps
from lcd import LcdApi                          # LCD API for display control
from pico_i2c_lcd import I2cLcd                 # I2C LCD library for controlling the LCD display
import network                                  # Network library for WiFi connectivity
import socket                                   # Socket library for creating a web server
from ds1302 import DS1302                       # DS1302 RTC library for real-time clock functionality

# 1. Setup WiFi
picoWifi = network.WLAN(network.STA_IF)
picoWifi.active(True)
picoWifi.connect("Aishaa's S25", "ayambakar1")

while not picoWifi.isconnected():
    print("connecting to wifi..")
    time.sleep(1)

print('Connected! IP:', picoWifi.ifconfig()[0])     # Print the assigned IP address to the console for reference

# 2. Setup Server Socket
addr = ('0.0.0.0', 5000)                # Listen on all interfaces, port 5000
picoSocket = socket.socket()            # Create a TCP socket, TCP is a connection-oriented protocol that ensures reliable data transmission between devices. It establishes a connection before transmitting data and guarantees that data packets are delivered in the correct order without loss or duplication.
picoSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Allow the socket to be reused immediately after the program is restarted, preventing "Address already in use" errors during development and testing.
picoSocket.bind(addr)                   # Bind the socket to the specified address and port, allowing it to listen for incoming connections on that port.
picoSocket.listen(1)                    # Start listening for incoming connections, allowing a backlog of 1 connection (the number of unaccepted connections that the system will allow before refusing new connections).
picoSocket.setblocking(False)           # Set the socket to non-blocking mode, allowing the program to continue executing even if there are no incoming connections, which is essential for maintaining responsiveness in the main loop while waiting for RFID scans and handling web requests simultaneously.

# Pin Definitions
sck_pin, mosi_pin, miso_pin = 14, 15, 12
sda_pin, rst_pin = 2, 17
led_green = Pin(11, Pin.OUT)
led_red = Pin(10, Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)   # 400kHz I2C frequency for faster communication with the LCD
buzzer = PWM(Pin(18))                               # PWM is used for controlling the buzzer's frequency and duration, allowing for different beep patterns to indicate various events (e.g., successful scan, error, etc.)

# RTC Setup
ds = DS1302(Pin(20), Pin(21), Pin(22))
# Set time once: [Year, Month, Day, DayOfWeek, Hour, Minute, Second]
# ds.date_time([2026, 4, 1, 3, 14, 11, 0])

reader = MRFC522(sck_pin, mosi_pin, miso_pin, rst_pin, sda_pin)
lcd = I2cLcd(i2c, 0x27, 2, 16)

allowed_users = {
    "0x71-0xa7-0x2f-0xaa-0x53": "Aisha",
    "0x6d-0x42-0x2d-0x1f-0x1d": "Vyshna",
}

# --- KEY DATA STORAGE ---
is_currently_in = {}  # Dictionary to track who is currently inside {UID: Time}
attendance_log = []   # List to store ALL scan history [{name, time, status}]

def play_beep(freq, duration_ms):       # Function to play a beep sound on the buzzer at a specified frequency and duration, providing auditory feedback for events such as successful scans or errors.
    buzzer.freq(freq)                   # Set the frequency of the buzzer to the specified value, allowing for different tones to indicate various events (e.g., a high-pitched beep for a successful scan and a low-pitched beep for an error).
    buzzer.duty_u16(30000)              # _u16 is 16 bit resolution, so 30000 is about 45% duty cycle, which is a good volume for the buzzer without being too loud.
    time.sleep_ms(duration_ms)          # Sleep for the specified duration in milliseconds while the buzzer is active, allowing the beep to be heard for the intended length of time.
    buzzer.duty_u16(0)                  # Turn off the buzzer by setting the duty cycle to 0, ensuring that it stops making sound after the specified duration.

lcd.putstr("Scan the RFID! \nThank you :)")

while True:
    # Get Time from RTC
    t = ds.date_time()      # t is a tuple in the format (Year, Month, Day, DayOfWeek, Hour, Minute, Second)

    # Standard format for DS1302 library: [Y, M, D, W, H, M, S]
    # If your library uses different order, adjust t[index] below
    h, m, s = t[4], t[5], t[6] % 60
    period = "AM" if h < 12 else "PM"
    display_hour = h % 12
    if display_hour == 0:
        display_hour = 12

    current_time = "{:02d}:{:02d}:{:02d} {}".format(display_hour, m, s, period)

    # Fix date too
    year  = 2000 + t[6]
    month = t[4]
    day   = t[3]

    full_date = "{:04d}-{:02d}-{:02d}".format(t[0], t[1], t[2]) # Format the date as YYYY-MM-DD for consistent logging and display, making it easier to read and sort the attendance records based on date. This format is widely used and recognized, ensuring clarity when reviewing the attendance history.

    # --- PART 1: RFID SCANNING ---
    (stat, tag_type) = reader.request(reader.REQIDL)        # Check for RFID tags in the vicinity using the REQIDL command, which detects tags that are not currently in a halt state (i.e., tags that are actively being scanned). The function returns a status code and the type of tag detected, allowing the program to proceed with reading the tag's UID if a tag is successfully detected.
    if stat == reader.OK:
        (stat, uid) = reader.anticoll()                     # reader.anticoll() is used to read the UID (Unique Identifier) of the detected RFID tag while also performing anti-collision detection to ensure that if multiple tags are present, it can still read one tag's UID without interference. The function returns a status code and the UID of the tag, allowing the program to identify which user is scanning their RFID card and proceed with the appropriate actions based on whether they are logging in or out.
        if stat == reader.OK:
            uid_str = "-".join([hex(i) for i in uid])       # Convert the UID list to a string format (e.g., "0x71-0xa7-0x2f-0xaa-0x53") for easier comparison with the allowed_users dictionary, allowing the program to check if the scanned UID corresponds to a known user and determine whether to log them in or out based on their current status in the is_currently_in dictionary.

            if uid_str in allowed_users:                    # Check if the scanned UID is in the allowed_users dictionary, which contains the UIDs of authorized users and their corresponding names. If the UID is found in the dictionary, it means that the user is recognized and can proceed with logging in or out based on their current status. If the UID is not found, it indicates an unauthorized scan, and the program will respond accordingly (e.g., displaying a "Go Away!" message and playing an error beep).
                user_name = allowed_users[uid_str]          # Retrieve the user's name from the allowed_users dictionary using the scanned UID as the key, allowing the program to personalize the welcome or goodbye message displayed on the LCD and to log the user's name in the attendance records for better tracking and reporting of attendance history.
                lcd.clear()

                if uid_str not in is_currently_in:          # Check if the user is currently not logged in (i.e., their UID is not in the is_currently_in dictionary). If the user is not currently logged in, it means they are scanning their RFID card to log in, and the program will proceed with the login actions (e.g., updating the is_currently_in dictionary, logging the attendance, displaying a welcome message, and playing a beep). If the user is already logged in (i.e., their UID is in the is_currently_in dictionary), it means they are scanning their RFID card to log out, and the program will proceed with the logout actions (e.g., removing their UID from the is_currently_in dictionary, logging the attendance, displaying a goodbye message, and playing a beep).
                    # --- ACTION: LOG IN ---
                    is_currently_in[uid_str] = current_time
                    attendance_log.append({"name": user_name, "time": current_time, "date": full_date, "status": "IN"})

                    lcd.putstr(f"Welcome {user_name} \nIn: {current_time}")
                    led_green.value(1)
                    play_beep(3500, 300)
                else:
                    # --- ACTION: LOG OUT ---
                    del is_currently_in[uid_str]
                    attendance_log.append({"name": user_name, "time": current_time, "date": full_date, "status": "OUT"})

                    lcd.putstr(f"Bye {user_name} \nOut: {current_time}")
                    led_red.value(1)
                    play_beep(3500, 300)
                    time.sleep_ms(50)
                    play_beep(3500, 350)

                time.sleep(2)
                led_green.value(0)
                led_red.value(0)
                lcd.clear()
                lcd.putstr("Scan the RFID! \nThank you :)")
            else:
                lcd.clear()
                lcd.putstr("Go Away!")
                led_red.value(1)
                play_beep(600, 700)
                time.sleep(1)
                led_red.value(0)
                lcd.clear()
                lcd.putstr("Scan the RFID! \nThank you :)")

    # --- PART 2: WEB SERVER ---
    try:
        cl, address = picoSocket.accept()
        cl.settimeout(0.5)
        request = cl.recv(1024)

        # Build History Rows (Latest first)
        history_rows = ""
        for entry in attendance_log[::-1]:
            color = "green" if entry['status'] == "IN" else "red"
            history_rows += f"<li>{entry['date']} | {entry['time']} - <b>{entry['name']}</b> (<span style='color:{color}'>{entry['status']}</span>)</li>"

        if not history_rows:
            history_rows = "<li>No scans recorded yet.</li>"

        response = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"><meta http-equiv="refresh" content="5">
            <title>Pico Attendance</title>
            <style>body{{font-family:sans-serif; padding:20px;}} ul{{list-style:none; padding:0;}} li{{padding:5px; border-bottom:1px solid #eee;}}</style>
        </head>
        <body>
            <h1>RFID Attendance System</h1>
            <p><b>Current Time:</b> {full_date} {current_time}</p>
            <hr>
            <h3>Activity History:</h3>
            <ul>{history_rows}</ul>
        </body>
        </html>"""

        cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
        cl.sendall(response)
        cl.close()
    except Exception:
        pass

    time.sleep(0.1)
