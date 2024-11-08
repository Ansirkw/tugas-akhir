import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel
import cv2
import dlib
import numpy as np
import motor
from sleepy_detector import SleepyDetectorThread

motor.maju()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.frame_queue

        # Set up the window
        self.setWindowTitle("Human Machine Interface")
        self.setGeometry(int(1280 / 4), int(720/4), 1280, 720)

        # Create a layout
        hbox = QHBoxLayout()

        vbox2 = QVBoxLayout()

        hbox.addLayout(self.first_column())
        hbox.addLayout(self.second_column())

        self.setLayout(hbox)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.sleepy_detector = SleepyDetectorThread()
        self.sleepy_detector.data_sleepy_detector.connect(self.update_frame)
        self.sleepy_detector.start()

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
        heading_sensor = QLabel("Sensor Ultrasonik 1")
        heading_sensor.setAlignment(Qt.AlignCenter)
        heading_status = QLabel("Status Ultrasonik 2")
        heading_status.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Getting status...")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(heading_sensor)
        layout.addWidget(heading_status)
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


if __name__ == "__main__":
# Main execution
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    app.exec_()

