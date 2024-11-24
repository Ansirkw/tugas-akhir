from RPi import GPIO
from .pin_config import PINS
from .gui import start_gui
from .motor import Motor
import time
import threading

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)

    # motor controls
    GPIO.setup(PINS['motor_kanan']['in1'],  GPIO.OUT)
    GPIO.setup(PINS['motor_kanan']['in2'],  GPIO.OUT)
    GPIO.setup(PINS['motor_kanan']['en_a'], GPIO.OUT)

    GPIO.setup(PINS['motor_kiri']['in3'],   GPIO.OUT)
    GPIO.setup(PINS['motor_kiri']['in4'],   GPIO.OUT)
    GPIO.setup(PINS['motor_kiri']['en_b'],  GPIO.OUT)

    # ultrasonik
    GPIO.setup(PINS['ultrasonik_1']['trigger'], GPIO.OUT)
    GPIO.setup(PINS['ultrasonik_1']['echo'],    GPIO.IN)
    GPIO.setup(PINS['ultrasonik_2']['trigger'], GPIO.OUT)
    GPIO.setup(PINS['ultrasonik_2']['echo'],    GPIO.IN)
    
def main():
    setup_gpio()
    # GPIO.cleanup()
    start_gui()
