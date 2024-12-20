import RPi.GPIO as GPIO
import time 

# Pin untuk sensor ultrasonik kedua
trigger_pin_2 = 20
echo_pin_2 = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin_2, GPIO.OUT)
GPIO.setup(echo_pin_2, GPIO.IN)

def send_trigger_pulse(trigger_pin):
    GPIO.output(trigger_pin, True)
    time.sleep(0.0001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(echo_pin, value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance(trigger_pin, echo_pin):
    send_trigger_pulse(trigger_pin)
    wait_for_echo(echo_pin, True, 10000)
    start = time.time()
    wait_for_echo(echo_pin, False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len / 0.000058
    return distance_cm

def get_status(distance):
    if 2 <= distance <= 6:
        return "Aman"
    else:
        return "PERINGATAN!"

try:
    while True:
        distance_2 = get_distance(trigger_pin_2, echo_pin_2)
        status_2 = get_status(distance_2)
        
        print("Distance from sensor 2: %f cm - Status: %s" % (distance_2, status_2))
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()
                                                                                      