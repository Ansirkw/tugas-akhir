import RPi.GPIO as GPIO
import time

# Konfigurasi pin untuk sensor 1
trigger_pin1 = 26
echo_pin1 = 19

# Konfigurasi pin untuk sensor 2
trigger_pin2 = 20
echo_pin2 = 16

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin1, GPIO.OUT)
GPIO.setup(echo_pin1, GPIO.IN)
GPIO.setup(trigger_pin2, GPIO.OUT)
GPIO.setup(echo_pin2, GPIO.IN)

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
    distance_in = distance_cm / 2.54
    return distance_cm, distance_in

try:
    while True:
        # Membaca jarak dari sensor 1
        distance1_cm, distance1_in = get_distance(trigger_pin1, echo_pin1)
        print("Sensor 1: cm=%f\tinches=%f" % (distance1_cm, distance1_in))
        
        # Membaca jarak dari sensor 2
        distance2_cm, distance2_in = get_distance(trigger_pin2, echo_pin2)
        print("Sensor 2: cm=%f\tinches=%f" % (distance2_cm, distance2_in))
        
        # Delay untuk pengulangan
        time.sleep(1)

except KeyboardInterrupt:
    print("Program dihentikan")
    GPIO.cleanup()
