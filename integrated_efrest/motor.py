import RPi.GPIO as GPIO
from .pin_config import PINS
import time

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
      

