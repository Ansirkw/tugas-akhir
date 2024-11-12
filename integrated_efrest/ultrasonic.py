import RPi.GPIO as GPIO
import time 
from PyQt5.QtCore import QThread, pyqtSignal
from .pin_config import PINS

class UltrasonicDetectionThread(QThread):
    data_ultrasonik = pyqtSignal(tuple)

    def run(self):
        while True:
            distance_1 = self.get_distance(PINS['ultrasonik_1']['trigger'], PINS['ultrasonik_1']['echo'])
            distance_2 = self.get_distance(PINS['ultrasonik_2']['trigger'], PINS['ultrasonik_2']['echo'])
            
            status_1 = self.get_status(distance_1)
            status_2 = self.get_status(distance_2)

            self.data_ultrasonik.emit(((distance_1, status_1), (distance_2, status_2)))
            time.sleep(0.1)

    def send_trigger_pulse(self, trigger_pin):
        GPIO.output(trigger_pin, True)
        time.sleep(0.0001)
        GPIO.output(trigger_pin, False)

    def wait_for_echo(self, echo_pin, value, timeout):
        count = timeout
        while GPIO.input(echo_pin) != value and count > 0:
            count = count - 1

    def get_distance(self, trigger_pin, echo_pin):
        self.send_trigger_pulse(trigger_pin)
        self.wait_for_echo(echo_pin, True, 10000)
        start = time.time()
        self.wait_for_echo(echo_pin, False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        
        return distance_cm
    
    def get_status(self, distance):
        if 10 <= distance <= 20:
            return False # aman
        else:
            return True # peringatan