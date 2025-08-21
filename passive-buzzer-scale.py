from machine import Pin, PWM
import time

# Passive buzzer pin (change if needed)
buzzer = PWM(Pin(16))

# Note frequencies (Hz)
NOTES = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "REST": 0
}

# Simple melody: C major scale up and down
MELODY = [
    ("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("F4", 0.3),
    ("G4", 0.3), ("A4", 0.3), ("B4", 0.3), ("C5", 0.5),
    ("B4", 0.3), ("A4", 0.3), ("G4", 0.3), ("F4", 0.3),
    ("E4", 0.3), ("D4", 0.3), ("C4", 0.5)
]

def play_tone(freq, duration):
    if freq == 0:  # Rest note
        buzzer.duty_u16(0)
    else:
        buzzer.freq(freq)
        buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty_u16(0)  # Silence between notes
    time.sleep(0.05)

def play_melody(melody):
    for note, duration in melody:
        play_tone(NOTES[note], duration)

try:
    print("Playing melody...")
    play_melody(MELODY)
    print("Done.")
finally:
    buzzer.deinit()
