import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

# Right Motor
in1 = 15
in2 = 14
en_a = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)

q = GPIO.PWM(en_a, 100)
q.start(75)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

try:
    # Create Infinite loop to read user input
    while True:
        # Get user Input
        user_input = input()

        # To see user's input
        # print(user_input)

        if user_input == 'w':
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            print("Forward")

        elif user_input == 's':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            print('Back')

        elif user_input == 'd':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            print('Right')

        elif user_input == 'a':
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            print('Left')

        # Press 'c' to exit the script
        elif user_input == 'c':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            print('Stop')

# If user presses CTRL-C
except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
    print("GPIO Clean up")
    