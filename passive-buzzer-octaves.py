from machine import Pin, PWM
import time

# Define notes (Hz)
NOTES = {
    'C4': 262,
    'D4': 294,
    'E4': 330,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,
    'C5': 523
}

# Play melody on passive buzzer
def play_melody(pin_number, melody, duration=0.3, octave_shift=0):
    buzzer = PWM(Pin(pin_number))
    for note in melody:
        if note == " ":
            buzzer.duty_u16(0)  # Rest
        else:
            freq = NOTES[note] * (2 ** octave_shift)  # Apply octave shift
            buzzer.freq(int(freq))
            buzzer.duty_u16(50000)  # Volume
        time.sleep(duration)
        buzzer.duty_u16(0)  # Stop between notes
        time.sleep(0.04)
    buzzer.deinit()

# Example melody
melody = ["C4", "E4", "G4", "C5"]

# Play normally
print("Normal octave:")
play_melody(16, melody, duration=0.1, octave_shift=0)

# Play 1 octave up
print("One octave up:")
play_melody(16, melody, duration=0.1, octave_shift=1)

# Play 1 octave down
print("One octave down:")
play_melody(16, melody, duration=0.1, octave_shift=-1)
