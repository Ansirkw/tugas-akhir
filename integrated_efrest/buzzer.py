import RPi.GPIO as GPIO
import time
from .pin_config import PINS
from PyQt5.QtCore import QThread, pyqtSignal


class BuzzThread(QThread):
    finished = pyqtSignal()

    def run(self):
        self.buzz(220, 0.5)

        self.finished.emit()
    
    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for _ in range(cycles):
            GPIO.output(PINS['buzzer'], True)
            time.sleep(delay)
            GPIO.output(PINS['buzzer'], False)
            time.sleep(delay)
