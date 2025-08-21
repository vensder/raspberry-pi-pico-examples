# pico_i2c_lcd.py

from machine import I2C
from time import sleep

class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self.display = 0x04
        self.init_lcd()

    def init_lcd(self):
        self.write_cmd(0x33)
        self.write_cmd(0x32)
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x06)
        self.write_cmd(0x01)
        sleep(0.005)

    def write_cmd(self, cmd):
        self.send(cmd, 0)

    def write_char(self, charvalue):
        self.send(charvalue, 1)

    def send(self, data, mode):
        high = mode | (data & 0xF0) | self.backlight
        low = mode | ((data << 4) & 0xF0) | self.backlight
        self.i2c.writeto(self.i2c_addr, bytes([high | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([high & ~0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([low | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([low & ~0x04]))

    def putstr(self, string):
        for char in string:
            self.write_char(ord(char))

    def clear(self):
        # LCD clear display
        self.write_cmd(0x01)
        sleep(0.002)

    def home(self):
        # Cursor to home
        self.write_cmd(0x02)
        sleep(0.002)

    def move_to(self, col, row):
        # Set DDRAM address: row0=0x00, row1=0x40
        if row < 0: row = 0
        if row > 1: row = 1
        addr = 0x80 | (0x40 * row + col)
        self.write_cmd(addr)

