from machine import Pin, I2C
import utime
from pico_i2c_lcd import I2cLcd  # or: from i2c_lcd import I2cLcd

# Init LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Change address if needed

# Settings
scroll_text_str = "Bed time!  "
scroll_delay = 0.3  # seconds

# Time variables
hour = 22
minute = 52
second = 0

# Prepare scrolling text buffer
padding = " " * 16
scroll_buffer = padding + scroll_text_str + padding
scroll_index = 0

while True:
    # --- CLOCK ON TOP LINE ---
    time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
    lcd.move_to(0, 0)
    lcd.putstr("Clock " + time_str)

    # --- SCROLLING TEXT ON BOTTOM LINE ---
    lcd.move_to(0, 1)
    lcd.putstr(scroll_buffer[scroll_index:scroll_index+16])
    scroll_index = (scroll_index + 1) % (len(scroll_buffer) - 15)

    # --- TICK TIME ---
    utime.sleep(scroll_delay)
    second += scroll_delay
    if second >= 60:
        second = 0
        minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    if hour >= 24:
        hour = 0
