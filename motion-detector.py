from machine import Pin, I2C, PWM
import utime
from pico_i2c_lcd import I2cLcd  # use your working driver
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
play_melody(16, melody, duration=0.1, octave_shift=0)

# Play 1 octave up
play_melody(16, melody, duration=0.1, octave_shift=1)

# Play 1 octave down
play_melody(16, melody, duration=0.1, octave_shift=-1)


# --- LCD Setup ---
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # adjust address if needed

# --- Buzzers ---
passive_buzzer = PWM(Pin(16))  # passive
active_buzzer = Pin(15, Pin.OUT)  # active

# --- PIR sensor ---
pir = Pin(28, Pin.IN)

# --- Clock start ---
hour = 12
minute = 0
second = 0

# --- Scrolling message ---
scroll_text_str = "Welcome to Pico Fun!  "
scroll_delay = 0.3
padding = " " * 16
scroll_buffer = padding + scroll_text_str + padding
scroll_index = 0

# --- Functions ---
def play_passive(freq, duration=0.2):
    if freq == 0:
        passive_buzzer.duty_u16(0)
    else:
        passive_buzzer.freq(freq)
        passive_buzzer.duty_u16(30000)
    utime.sleep(duration)
    passive_buzzer.duty_u16(0)
    utime.sleep(0.05)

def beep_active(duration=0.2):
    active_buzzer.on()
    utime.sleep(duration)
    active_buzzer.off()
    utime.sleep(0.05)

# --- Main loop ---
while True:
    # --- CLOCK TOP LINE ---
    time_str = "{:02}:{:02}:{:02}".format(hour, minute, int(second))
    lcd.move_to(0, 0)
    lcd.putstr("Clock " + time_str)

    # --- SCROLLING MESSAGE BOTTOM LINE ---
    lcd.move_to(0, 1)
    lcd.putstr(scroll_buffer[scroll_index:scroll_index+16])
    scroll_index = (scroll_index + 1) % (len(scroll_buffer) - 15)

    # --- PIR MOTION CHECK ---
    if pir.value() == 1:
        lcd.move_to(0, 1)
        lcd.putstr("Motion detected!  ")  # overwrite scroll line
        play_passive(880*3, 0.2)  # short tone
        utime.sleep(0.5)  # wait a little so it doesn’t repeat too fast
        beep_active(0.1)
        utime.sleep(0.5)  # wait a little so it doesn’t repeat too fast

        # Play normally
        play_melody(16, melody, duration=0.1, octave_shift=0)

        # Play 1 octave up
        play_melody(16, melody, duration=0.1, octave_shift=1)

        # Play 1 octave down
        play_melody(16, melody, duration=0.1, octave_shift=-1)

        utime.sleep(0.5)  # wait a little so it doesn’t repeat too fast

    # --- Tick time ---
    utime.sleep(scroll_delay)
    second += scroll_delay
    if second >= 60:
        second = 0
        minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    if hour >= 24:
        hour = 0
