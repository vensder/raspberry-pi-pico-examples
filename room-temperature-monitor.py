from machine import Pin, I2C
import dht
import utime
from pico_i2c_lcd import I2cLcd  # assuming you have the pico_i2c_lcd library

# --- Setup LCD ---
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # (I2C, address, rows, cols)

# --- Setup DHT22 sensor ---
dht_sensor = dht.DHT22(Pin(2))  # GP2

lcd.clear()
lcd.putstr("Room Monitor")

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        
        # Print to console
        print("Temp:", temp, "C   Hum:", hum, "%")
        
        # Display on LCD
        lcd.move_to(0, 1)  # second line
        lcd.putstr("T:{:.1f}C H:{:.1f}%".format(temp, hum))
        
    except Exception as e:
        print("Sensor error:", e)
    
    utime.sleep(2)
