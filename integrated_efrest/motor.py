import RPi.GPIO as GPIO
from .pin_config import PINS
from PyQt5.QtCore import QThread

class Motor:
   def setup(speed):
      pwm_a = GPIO.PWM(PINS["motor_kanan"]["en_a"], 100)
      pwm_b = GPIO.PWM(PINS["motor_kiri"]["en_b"], 100)
      pwm_a.start(speed)
      pwm_b.start(speed)

      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

      return (pwm_a, pwm_b)

   def maju():
      GPIO.output(PINS["motor_kanan"]["in1"], GPIO.HIGH)
      GPIO.output(PINS["motor_kanan"]["in2"], GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"], GPIO.HIGH)
      GPIO.output(PINS["motor_kiri"]["in3"], GPIO.LOW)

   def mundur():
      print('mundur')
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.HIGH)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.HIGH)

   def kanan():
      print('belok kanan')
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.HIGH)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

   def kiri():
      print('belok kiri')
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.HIGH)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

   def berhenti():
      print('berhenti')
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)
      
class MotorThread(QThread):
    running = False
    def __init__(self, move, speed):
        super(QThread, self).__init__()
        self.move = move
        self.speed = speed


    def run(self):
        _ = Motor.setup(self.speed)
        self.running = True
        while self.running:
            if (self.move == "maju"):
                Motor.maju()
            elif (self.move == "mundur"):
                Motor.mundur()
            elif (self.move == "kiri"):
                Motor.kiri()
            elif (self.move == "kanan"):
                Motor.kanan()
            elif (self.move == "berhenti"):
                Motor.berhenti()
        Motor.berhenti()
