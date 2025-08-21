from machine import Pin, I2C, PWM
import utime
import time
import dht

# from pico_i2c_lcd import I2cLcd  # use your working driver
from i2c_lcd import I2cLcd

# --- DHT22 setup (GP2) ---
### DHT22 ADDED ###
dht_sensor = dht.DHT22(Pin(2))

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

LOUD_BEEP = False
SERVO_ENABLED = False

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
hour, minute, second = 12, 0, 0

# --- Scrolling message ---
scroll_text_str = "Welcome to Pico Fun!  "
scroll_delay = 0.3
padding = " " * 16
scroll_buffer = padding + scroll_text_str + padding
scroll_index = 0

motion_message_timeout = 2  # seconds to keep motion message
last_motion_display = 0

# --- Backlight timing ---
off_timeout = 30       # seconds before full off
last_motion_time = utime.time()

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

def update_backlight():
    idle_time = utime.time() - last_motion_time
    if idle_time >= off_timeout:
        lcd.backlight_off()   # turn LCD off after timeout
    else:
        lcd.backlight_on()    # ensure LCD is on when motion detected

# --- Servo setup (on GP14) ---
servo = PWM(Pin(14))
servo.freq(50)

def set_angle(angle):
    # Adjust these values if your servo moves incorrectly
    min_duty = 1638   # ~0.5ms pulse
    max_duty = 8192   # ~2.5ms pulse
    duty = int(min_duty + (max_duty - min_duty) * angle / 180)
    servo.duty_u16(duty)

def angle_to_duty(angle):
    # Map 0–180° to duty (for 50Hz PWM, SG90 typically 0.5–2.5ms pulse)
    return int(((angle / 180) * 5000) + 2500)

def move_servo_smooth(current_angle, target_angle, step=1, delay=0.01):
    if current_angle < target_angle:
        for angle in range(current_angle, target_angle + 1, step):
            servo.duty_u16(angle_to_duty(angle))
            time.sleep(delay)
    else:
        for angle in range(current_angle, target_angle - 1, -step):
            servo.duty_u16(angle_to_duty(angle))
            time.sleep(delay)
    return target_angle

# Move servo to initial position
if SERVO_ENABLED:
    pos = 0
    target_angle = 100
    pos = move_servo_smooth(pos, target_angle, step=1, delay=0.01)
    utime.sleep(0.5)  # Allow servo to settle


# --- Main loop ---
while True:
    current_time = utime.time()

    # --- PIR MOTION CHECK ---
    if pir.value() == 1:
        last_motion_time = current_time
        lcd.backlight_on()  # bright when motion
        lcd.move_to(0, 1)
        lcd.putstr("Motion detected!  ")  # overwrite scroll line
        last_motion_display = utime.time()

        if SERVO_ENABLED:
            pos = move_servo_smooth(pos, 100, step=1, delay=0.01)
            utime.sleep(0.5)

        if LOUD_BEEP:
            play_passive(880*3, 0.1)  # short tone
            beep_active(0.1)
        else:
            for d in [0.1, 0.1, 0.2]:
                play_passive(880*3, d)
        utime.sleep(0.5)  # wait a little so it doesn’t repeat too fast    

        # Play normally
        play_melody(16, melody, duration=0.1, octave_shift=0)
        # Play 1 octave up
        play_melody(16, melody, duration=0.1, octave_shift=1)
        # Play 1 octave down
        play_melody(16, melody, duration=0.1, octave_shift=-1)
        utime.sleep(0.5)  # wait a little so it doesn’t repeat too fast

        if SERVO_ENABLED:
            pos = move_servo_smooth(pos, 0, step=1, delay=0.01)
            utime.sleep(0.5)


    # --- Update backlight based on idle time ---
    update_backlight()

    # --- CLOCK TOP LINE ---
    lcd.move_to(0, 0)   # ensure cursor at start of line
    time_str = "{:02}:{:02}:{:02}".format(hour, minute, int(second))
    lcd.putstr("Clock " + time_str)

    # --- DHT22 reading instead of scrolling ---
    ### DHT22 ADDED ###
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        lcd.move_to(0, 1)  # second line
        line = "T:{:.1f}C H:{:.1f}%".format(temp, hum)
        lcd.putstr(line)  # pad to 16 chars
    except:
        lcd.move_to(0, 1)
        lcd.putstr("Sensor Error   ")

    # --- Tick time ---
    utime.sleep(2)   # update sensor every 2 sec
    second += 2
    if second >= 60:
        second = 0
        minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    if hour >= 24:
        hour = 0

    # # --- SCROLLING MESSAGE BOTTOM LINE ---
    # if utime.time() - last_motion_display > motion_message_timeout:
    #     lcd.move_to(0, 1)
    #     lcd.putstr(scroll_buffer[scroll_index:scroll_index+16])
    #     scroll_index = (scroll_index + 1) % (len(scroll_buffer) - 15)

    # # --- Tick time ---
    # utime.sleep(scroll_delay)
    # second += scroll_delay
    # if second >= 60:
    #     second = 0
    #     minute += 1
    # if minute >= 60:
    #     minute = 0
    #     hour += 1
    # if hour >= 24:
    #     hour = 0
