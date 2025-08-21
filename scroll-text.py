from machine import Pin, I2C
from time import sleep
from i2c_lcd import I2cLcd

# Setup I2C and LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Adjust address if needed

def scroll_text(text, row=0, delay=0.3):
    """Scroll text across the LCD row"""
    lcd.clear()
    text = " " * 16 + text + " " * 16  # padding
    for i in range(len(text) - 15):
        lcd.clear()
        lcd.putstr(text[i:i+16])
        sleep(delay)

# Example usage
while True:
    scroll_text("Slap! Slap! Slap!", row=0, delay=0.25)
