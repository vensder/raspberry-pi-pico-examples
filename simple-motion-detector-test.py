from machine import Pin
import time

pir = Pin(28, Pin.IN)  # PIR OUT connected to GP28

print("PIR Module Test")
time.sleep(2)  # PIR stabilization time

while True:
    if pir.value() == 1:
        print("Motion detected!")
    else:
        print("No motion")
    time.sleep(0.5)
