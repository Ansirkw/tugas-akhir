import RPi.GPIO as GPIO
from .pin_config import PINS

class Motor:
   def setup():
      q = GPIO.PWM(PINS["motor_kanan"]["en_a"], 100)
      p = GPIO.PWM(PINS["motor_kiri"]["en_b"], 100)
      p.start(75)
      q.start(75)

      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

   def maju():
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.HIGH)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.HIGH)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

   def mundur():
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.HIGH)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.HIGH)

   def kanan():
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.HIGH)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

   def kiri():
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.HIGH)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)

   def berhenti():
      GPIO.output(PINS["motor_kanan"]["in1"],GPIO.LOW)
      GPIO.output(PINS["motor_kanan"]["in2"],GPIO.LOW)

      GPIO.output(PINS["motor_kiri"]["in4"],GPIO.LOW)
      GPIO.output(PINS["motor_kiri"]["in3"],GPIO.LOW)
      

