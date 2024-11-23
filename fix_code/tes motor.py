import RPi.GPIO as GPIO
import time

# Konfigurasi pin
IN1 = 15
IN2 = 14
IN3 = 7
IN4 = 8
ENA = 6
ENB = 10

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)

# Setup pin IN dan EN sebagai output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Setup PWM untuk kecepatan motor
pwmA = GPIO.PWM(ENA, 100)  # PWM pada ENA dengan frekuensi 100Hz
pwmB = GPIO.PWM(ENB, 100)  # PWM pada ENB dengan frekuensi 100Hz

# Mulai PWM
pwmA.start(0)  # Kecepatan awal 0
pwmB.start(0)  # Kecepatan awal 0

# Fungsi untuk motor A
def motorA_forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed)

def motorA_backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed)

def motorA_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(0)

# Fungsi untuk motor B
def motorB_forward(speed):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speed)

def motorB_backward(speed):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speed)

def motorB_stop():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwmB.ChangeDutyCycle(0)

# Program utama
try:
    while True:
        command = input("Masukkan perintah (w: maju, s: mundur, c: berhenti): ").strip().lower()
        if command == 'w':
            print("Truk maju dengan kecepatan 50%")
            motorA_forward(100)
            motorB_forward(100)
        elif command == 's':
            print("Truk mundur dengan kecepatan 50%")
            motorA_backward(50)
            motorB_backward(50)
        elif command == 'c':
            print("Menghentikan truk")
            motorA_stop()
            motorB_stop()
        else:
            print("Perintah tidak dikenali, masukkan 'w', 's', atau 'c'.")

except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    # Bersihkan GPIO
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
