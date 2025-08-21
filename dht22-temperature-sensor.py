import time
import machine
import dht

PIN = 2
p = machine.Pin(PIN, machine.Pin.IN, machine.Pin.PULL_UP)

def try_sensor(cls, tries=3, wait=2):
    s = cls(p)
    # give sensor a moment after power-up
    time.sleep(2)
    for i in range(tries):
        try:
            s.measure()
            t = s.temperature()
            h = s.humidity()
            print(cls.__name__, "OK:", t, "C", h, "%")
            return (t, h)
        except Exception as e:
            print(cls.__name__, "read failed:", e)
            time.sleep(wait)
    return None

print("Testing DHT on GP%d..." % PIN)
res = try_sensor(dht.DHT22)
if res is None:
    print("Trying DHT11...")
    res = try_sensor(dht.DHT11)

if res is None:
    print("No luck yet. Check wiring and try adding a 10k pull-up OUT→3V3 (some boards still need it).")
else:
    print("Reading succeeded.")
