from machine import Pin, I2C
import utime
from pico_i2c_lcd import I2cLcd  # your working driver

# Init LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # use your detected I2C address

def display_clock():
    # Fake clock start time (HH, MM, SS)
    hour = 12
    minute = 0
    second = 0

    while True:
        # Format time as HH:MM:SS
        time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
        lcd.move_to(0, 0)
        lcd.putstr("Clock:")
        lcd.move_to(0, 1)
        lcd.putstr(time_str + "      ")

        utime.sleep(1)
        second += 1
        if second == 60:
            second = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1
        if hour == 24:
            hour = 0

display_clock()
