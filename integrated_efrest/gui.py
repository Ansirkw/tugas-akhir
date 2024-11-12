import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel
import numpy as np
from .sleepy_detector import SleepyDetectorThread
from .ultrasonic import UltrasonicDetectionThread

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Human Machine Interface")
        self.setGeometry(int(1280 / 4), int(720/4), 1280, 720)

        # Create a layout
        hbox = QHBoxLayout()

        vbox2 = QVBoxLayout()

        hbox.addLayout(self.first_column())
        hbox.addLayout(self.second_column())

        self.setLayout(hbox)

        self.sleepy_detector = SleepyDetectorThread()
        self.sleepy_detector.data_sleepy_detector.connect(self.update_frame)
        self.sleepy_detector.start()

        
        self.sensor_ultrasonik = UltrasonicDetectionThread()
        self.sensor_ultrasonik.data_ultrasonik.connect(self.update_sensor_ultrasonik)
        self.sensor_ultrasonik.start()

    def first_column(self):
        layout = QVBoxLayout()

        heading = QLabel("Kontrol Truk")
        hbox = QHBoxLayout()
        
        button_maju = QPushButton("Maju")
        button_mundur = QPushButton("Mundur")   

        hbox.addWidget(button_maju)
        hbox.addWidget(button_mundur)

        layout.addWidget(heading)
        layout.addLayout(hbox)

        self.image_label = QLabel("Starting camera...")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        return layout 
    
    def second_column(self):
        layout = QVBoxLayout()
        heading_sensor_1 = QLabel("Sensor Ultrasonik 1")
        heading_sensor_1.setAlignment(Qt.AlignCenter)
        container_sensor_1 = QHBoxLayout()

        self.distance_sensor_1 = QLabel("Getting distance...")
        self.status_sensor_1 = QLabel("Getting status...")

        container_sensor_1.addWidget(self.distance_sensor_1)
        container_sensor_1.addWidget(self.status_sensor_1)

        heading_sensor_2 = QLabel("Sensor Ultrasonik 2")
        heading_sensor_2.setAlignment(Qt.AlignCenter)
        container_sensor_2 = QHBoxLayout()

        self.distance_sensor_2 = QLabel("Getting distance...")
        self.status_sensor_2 = QLabel("Getting status...")

        container_sensor_2.addWidget(self.distance_sensor_2)
        container_sensor_2.addWidget(self.status_sensor_2)


        self.status_label = QLabel("Getting status...")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(heading_sensor_1)
        layout.addLayout(container_sensor_1)
        layout.addWidget(heading_sensor_2)
        layout.addLayout(container_sensor_2)
        layout.addWidget(self.status_label)

        return layout
        
    def update_frame(self, data):
        # Get the image dimensions
        img, warning = data

        height, width, channel = img.shape
        bytes_per_line = 3 * width

        # Convert the OpenCV image to QImage
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # Set the QImage in the QLabel
        self.image_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.image_label.size(), Qt.KeepAspectRatio))

        if warning:
            self.status_label.setText("Limited")
        else:
            self.status_label.setText("Normal")

    def update_sensor_ultrasonik(self, data):
        sensor_1, sensor_2 = data
        distance_1, status_1 = sensor_1
        distance_2, status_2 = sensor_2

        self.distance_sensor_1.setText("Jarak: " + str(distance_1))

        if status_1:
            self.status_sensor_1.setText("Status: Bahaya")
        else:    
            self.status_sensor_1.setText("Status: Aman")

        self.distance_sensor_2.setText("Jarak: " + str(distance_2))

        if status_2:
            self.status_sensor_2.setText("Status: Bahaya")
        else:
            self.status_sensor_2.setText("Status: Aman")


def start_gui():
    # Main execution
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    app.exec_()

# if __name__ == "__main__":
    # start_gui()
    