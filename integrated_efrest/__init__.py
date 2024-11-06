from RPi import GPIO
from pin_config import PINS
import motor

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # motor controls
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINS["motor_kanan"]["in1"],GPIO.OUT)
    GPIO.setup(PINS["motor_kanan"]["in2"],GPIO.OUT)
    GPIO.setup(PINS["motor_kanan"]["en_a"],GPIO.OUT)

    GPIO.setup(PINS["motor_kiri"]["in3"],GPIO.OUT)
    GPIO.setup(PINS["motor_kiri"]["in4"],GPIO.OUT)
    GPIO.setup(PINS["motor_kiri"]["en_b"],GPIO.OUT)

    motor.setup()
    
def main():
    setup_gpio()
