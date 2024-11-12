import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QSizePolicy
import numpy as np
from .motor import Motor
from .sleepy_detector import SleepyDetectorThread
from .ultrasonic import UltrasonicDetectionThread
from collections import deque

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.status_queue = deque(maxlen=2)
        self.control_is_enabled = True
        self.grace_period = False

        self.setWindowTitle("Human Machine Interface")
        self.setGeometry(int(1280 / 4), int(720/4), 1280, 720)
        self.setStyleSheet("font-size: 24px")

        hbox = QGridLayout()
        hbox.setSpacing(10)

        hbox.addLayout(self.create_truck_control(), 0, 0)
        hbox.addLayout(self.create_ultrasonic_sensor(), 0, 1)
        hbox.addLayout(self.create_sleepy_detection(), 1, 0)
        hbox.addLayout(self.create_status(), 1, 1)

        self.setLayout(hbox)

        self.sleepy_detector = SleepyDetectorThread()
        self.sleepy_detector.data_sleepy_detector.connect(self.update_frame)
        self.sleepy_detector.start()

        
        self.sensor_ultrasonik = UltrasonicDetectionThread()
        self.sensor_ultrasonik.data_ultrasonik.connect(self.update_sensor_ultrasonik)
        self.sensor_ultrasonik.start()

    def create_truck_control(self):
        layout = QVBoxLayout()
        heading = QLabel("Kontrol Truk")
        heading.setStyleSheet("font-weight: bold")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout = QGridLayout()
        
        self.button_maju = QPushButton("Maju")
        self.button_mundur = QPushButton("Mundur")   
        self.button_kiri = QPushButton("Belok Kiri")   
        self.button_kanan = QPushButton("Belok Kanan")
        self.button_berhenti = QPushButton("Berhenti")
        self.button_lepas_rem = QPushButton("Lepas Rem")

        self.button_maju.clicked.connect(Motor.maju)
        self.button_mundur.clicked.connect(Motor.mundur)
        self.button_kiri.clicked.connect(Motor.kiri)
        self.button_kanan.clicked.connect(Motor.kanan)
        self.button_berhenti.clicked.connect(Motor.berhenti)
        self.button_lepas_rem.clicked.connect(self.set_start_grace_period)  # Trigger async function


        control_layout.addWidget(self.button_maju, 0, 0)
        control_layout.addWidget(self.button_mundur, 0, 1)
        control_layout.addWidget(self.button_kiri, 1, 0)
        control_layout.addWidget(self.button_kanan, 1, 1)
        control_layout.addWidget(self.button_berhenti, 2, 0)
        control_layout.addWidget(self.button_lepas_rem, 2, 1)

        layout.addWidget(heading)
        layout.addLayout(control_layout)
        return layout
    
    def create_ultrasonic_sensor(self):
        layout = QVBoxLayout()
        heading_sensor_1 = QLabel("Sensor Ultrasonik 1")
        heading_sensor_1.setStyleSheet("font-weight: bold")
        heading_sensor_1.setAlignment(Qt.AlignCenter)
        container_sensor_1 = QHBoxLayout()

        self.distance_sensor_1 = QLabel("Getting distance...")
        self.status_sensor_1 = QLabel("Getting status...")

        container_sensor_1.addWidget(self.distance_sensor_1)
        container_sensor_1.addWidget(self.status_sensor_1)

        heading_sensor_2 = QLabel("Sensor Ultrasonik 2")
        heading_sensor_2.setStyleSheet("font-weight: bold")
        heading_sensor_2.setAlignment(Qt.AlignCenter)
        container_sensor_2 = QHBoxLayout()

        self.distance_sensor_2 = QLabel("Getting distance...")
        self.status_sensor_2 = QLabel("Getting status...")

        container_sensor_2.addWidget(self.distance_sensor_2)
        container_sensor_2.addWidget(self.status_sensor_2)

        layout.addWidget(heading_sensor_1)
        layout.addLayout(container_sensor_1)
        layout.addWidget(heading_sensor_2)
        layout.addLayout(container_sensor_2)
        return layout


    def create_sleepy_detection(self):
        layout = QVBoxLayout()
        heading = QLabel("Live Feed")
        heading.setStyleSheet("font-weight: bold")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel("Starting camera...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        layout.addWidget(heading)
        layout.addWidget(self.image_label)

        return layout 
    
    def create_status(self):
        layout = QVBoxLayout()
        heading = QLabel("Car Status")
        heading.setStyleSheet("font-weight: bold")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Getting status...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        
        layout.addWidget(heading)
        layout.addWidget(self.status_label)

        return layout
        
    def update_frame(self, data):
        # Get the image dimensions
        img, warning = data

        height, width, _ = img.shape
        bytes_per_line = 3 * width

        # Convert the OpenCV image to QImage
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        self.image_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.image_label.size(), Qt.KeepAspectRatio))

        if warning:
            self.status_queue.append("Limited")
        else:
            self.status_queue.append("Normal")
        
        self.update_display_status()

    def update_sensor_ultrasonik(self, data):
        sensor_1, sensor_2 = data
        distance_1, status_1 = sensor_1
        distance_2, status_2 = sensor_2

        self.distance_sensor_1.setText(f"Jarak: {distance_1:.2f}")
        self.status_sensor_1.setText("Status: Bahaya" if status_1 else "Status: Aman")
        self.distance_sensor_2.setText(f"Jarak: {distance_2:.2f}")
        self.status_sensor_2.setText("Status: Bahaya" if status_2 else "Status: Aman")

        status_2 = False
        if status_1 or status_2:
            self.status_queue.append("Stopped")

        self.update_display_status()

    def update_display_status(self):
        if "Stopped" in self.status_queue:
            self.status_label.setText("Stopped")
            self.status_label.setStyleSheet("background-color: red; color: white")
            if not self.grace_period and self.control_is_enabled:
                self.toggle_controls()
        elif "Limited" in self.status_queue:
            self.status_label.setText("Limited")
            self.status_label.setStyleSheet("background-color: yellow; color: black")
        else:
            if not self.control_is_enabled:
                self.toggle_controls()
            self.status_label.setText("Normal")
            self.status_label.setStyleSheet("background-color: green; color: white")

    def toggle_controls(self):
        self.control_is_enabled = not self.control_is_enabled
        self.button_maju.setEnabled(self.control_is_enabled)
        self.button_mundur.setEnabled(self.control_is_enabled)
        self.button_kiri.setEnabled(self.control_is_enabled)
        self.button_kanan.setEnabled(self.control_is_enabled)
        self.button_berhenti.setEnabled(self.control_is_enabled)

    # BELUM BISA
    def set_start_grace_period(self):
        self.grace_period = not self.grace_period    
        current_state = self.button_lepas_rem.isEnabled()
        self.button_lepas_rem.setEnabled(not current_state)
        self.toggle_controls()

        print(current_state)
        if self.grace_period:
            QTimer.singleShot(5000, self.toggle_grace_period)

    def toggle_grace_period(self):
        self.grace_period = not self.grace_period

def start_gui():
    # Main execution
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    app.exec_()

# if __name__ == "__main__":
    # start_gui()
    