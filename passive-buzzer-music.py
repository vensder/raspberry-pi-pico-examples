from machine import Pin, PWM
import utime

buzzer = PWM(Pin(16))  # GP16 - passive buzzer

def tone(freq, duration):
    buzzer.freq(freq)
    buzzer.duty_u16(30000)  # volume
    utime.sleep(duration)
    buzzer.duty_u16(0)

# Example: simple melody
melody = [(440, 0.3), (494, 0.3), (523, 0.3), (0, 0.3)]
for freq, dur in melody:
    if freq > 0:
        tone(freq, dur)
    else:
        utime.sleep(dur)

buzzer.deinit()
