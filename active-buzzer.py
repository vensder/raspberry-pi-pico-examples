from machine import Pin
import time

# Change the pin to the one you want to test
buzzer_pin = Pin(15, Pin.OUT) # Active buzzer

buzzer_pin.value(1)  # Turn ON
time.sleep(0.1)        # 2 seconds sound
buzzer_pin.value(0)  # Turn OFF
