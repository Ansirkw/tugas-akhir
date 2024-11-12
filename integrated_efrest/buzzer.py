import RPi.GPIO as GPIO
import time
from .pin_config import PINS

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for _ in range(cycles):
        GPIO.output(PINS['buzzer'], True)
        time.sleep(delay)
        GPIO.output(PINS['buzzer'], False)
        time.sleep(delay)