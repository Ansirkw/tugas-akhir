import sys
import RPi.GPIO as GPIO
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QSizePolicy
from .motor import MotorThread
from .sleepy_detector import SleepyDetectorThread
from .ultrasonic import UltrasonicDetectionThread
from .buzzer import BuzzThread
from collections import deque
                
# Human Machine Interface (HMI) untuk Integrated EFREST
class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Antrian status untuk handle perubahan status dari beberapa sensor
        self.status_queue = deque(maxlen=2)

        # States
        self.control_is_enabled = True
        self.is_lepas_rem = False

        # Pengaturan layar utama
        self.setWindowTitle("Human Machine Interface")
        self.setGeometry(int(1280 / 4), int(720/4), 1280, 720)
        self.setStyleSheet("font-size: 24px")

        # Layout utama layar
        main_layout = QGridLayout()
        main_layout.setSpacing(10)

        main_layout.addLayout(self.create_truck_control_layout(), 0, 0)
        main_layout.addLayout(self.create_ultrasonic_data_layout(), 0, 1)
        main_layout.addLayout(self.create_sleepy_detection_layout(), 1, 0)
        main_layout.addLayout(self.create_status_layout(), 1, 1)
        self.setLayout(main_layout)

        # Jalankan thread untuk sleepy detector
        self.sleepy_detector = SleepyDetectorThread()
        self.sleepy_detector.data_sleepy_detector.connect(self.update_frame)
        self.sleepy_detector.start()

        # Jalani=kan thread untuk sensor ultrasonic
        self.sensor_ultrasonik = UltrasonicDetectionThread()
        self.sensor_ultrasonik.data_ultrasonik.connect(self.update_sensor_ultrasonik)
        self.sensor_ultrasonik.start()
        
        self.speed = 100
        self.motor_thread = None

        self.buzz_thread = None

    def start_control_motor_thread(self, move):
        if self.motor_thread is None:
            self.motor_thread = MotorThread(move=move, speed=self.speed)
            self.motor_thread.start()

    def stop_control_motor_thread(self):
        if self.motor_thread:
            self.motor_thread.running = False
            self.motor_thread.quit()
            self.motor_thread.wait()
            self.motor_thread = None
    
    def change_motor_thread_speed(self):
        if self.motor_thread:
            self.motor_thread.speed = self.speed
    
    def start_buzz_thread(self):
        if self.buzz_thread is None:
            self.buzz_thread = BuzzThread()
            self.buzz_thread.finished.connect(self.stop_buzz_thread)
            self.buzz_thread.start()
    
    def stop_buzz_thread(self):
        if self.buzz_thread:
            self.buzz_thread.quit()
            self.buzz_thread.wait()
            self.buzz_thread = None

    # Layout untuk kontrol truk
    def create_truck_control_layout(self):
        layout = QVBoxLayout()
        heading = QLabel("Kontrol Truk")
        heading.setStyleSheet("font-weight: bold")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout = QGridLayout()
        
        self.button_maju = QPushButton("Maju")
        self.button_mundur = QPushButton("Mundur")   
        self.button_kiri = QPushButton("Belok Kiri")   
        self.button_kanan = QPushButton("Belok Kanan")
        self.button_lepas_rem = QPushButton("Lepas Rem")
        self.button_lepas_rem.setEnabled(False)

        self.button_maju.pressed.connect(lambda: self.start_control_motor_thread("maju"))
        self.button_maju.released.connect(self.stop_control_motor_thread)
        self.button_mundur.pressed.connect(lambda: self.start_control_motor_thread("mundur"))
        self.button_mundur.released.connect(self.stop_control_motor_thread)
        self.button_kiri.pressed.connect(lambda: self.start_control_motor_thread("kiri"))
        self.button_kiri.released.connect(self.stop_control_motor_thread)
        self.button_kanan.pressed.connect(lambda: self.start_control_motor_thread("kanan"))
        self.button_kanan.released.connect(self.stop_control_motor_thread)
        self.button_lepas_rem.clicked.connect(self.lepas_rem)

        self.ear_score = QLabel("Calculating...")

        control_layout.addWidget(self.button_maju, 0, 0)
        control_layout.addWidget(self.button_mundur, 0, 1)
        control_layout.addWidget(self.button_kiri, 1, 0)
        control_layout.addWidget(self.button_kanan, 1, 1)
        control_layout.addWidget(self.ear_score, 2, 0)
        control_layout.addWidget(self.button_lepas_rem, 2, 1)

        layout.addWidget(heading)
        layout.addLayout(control_layout)
        return layout

    # Layout untuk tampilan data dari sensor ultrasonik
    def create_ultrasonic_data_layout(self):
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

    # Layout untuk live feed camera dan sleepy detection
    def create_sleepy_detection_layout(self):
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
    
    # Layout untuk tampilan status
    def create_status_layout(self):
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
    
    # Update image di sleepy_detection layout
    def update_frame(self, data):
        # Ambil dimensi dari gambar
        img, warning, ear_score = data

        height, width, _ = img.shape
        bytes_per_line = 3 * width

        # Konversi gambar OpenCV menjadi QImage
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # Tampilkan pada image_label
        self.image_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.image_label.size(), Qt.KeepAspectRatio))

        # Pengecekan status
        if warning:
            self.status_queue.append("Stopped")
        else:
            self.status_queue.append("Normal")
        
        self.ear_score.setText(f"EAR: {ear_score:.2f}")
        
        self.update_display_status()

    # Updata teks untuk data sensor ultrasonik
    def update_sensor_ultrasonik(self, data):
        sensor_1, sensor_2 = data
        distance_1, status_1 = sensor_1
        distance_2, status_2 = sensor_2

        self.distance_sensor_1.setText(f"Jarak: {distance_1:.2f}")
        self.status_sensor_1.setText("Status: Bahaya" if status_1 else "Status: Aman")
        self.distance_sensor_2.setText(f"Jarak: {distance_2:.2f}")
        self.status_sensor_2.setText("Status: Bahaya" if status_2 else "Status: Aman")

        if status_1 or status_2:
            self.status_queue.append("Stopped")

        self.update_display_status()

    # Sesuai namanya
    def update_display_status(self):
        if self.is_lepas_rem:
            self.status_label.setText("Mode Lepas Rem")
            self.status_label.setStyleSheet("background-color: orange; color: white")
        elif "Stopped" in self.status_queue:
            self.status_label.setText("Stopped")
            self.status_label.setStyleSheet("background-color: red; color: white")
            if self.control_is_enabled:
                self.toggle_controls()
        else:
            self.status_label.setText("Normal")
            self.status_label.setStyleSheet("background-color: green; color: white")
            if not self.control_is_enabled:
                self.toggle_controls()
            self.speed = 100
            self.change_motor_thread_speed()

    def keyPressEvent(self, e):
        if e.text() == "w":
            self.start_control_motor_thread("maju")
        elif e.text() == "s":   
            self.start_control_motor_thread("mundur")
        elif e.text() == "a":   
            self.start_control_motor_thread("kiri")
        elif e.text() == "d":   
            self.start_control_motor_thread("kanan")

    def keyReleaseEvent(self, e):
        if e.text() in "wsad":
            self.stop_control_motor_thread()
            

    # Fungsi untuk mengaktifkan dan menonaktifkan kontrol
    def toggle_controls(self):
        self.control_is_enabled = not self.control_is_enabled
        self.button_maju.setEnabled(self.control_is_enabled)
        self.button_mundur.setEnabled(self.control_is_enabled)
        self.button_kiri.setEnabled(self.control_is_enabled)
        self.button_kanan.setEnabled(self.control_is_enabled)
        self.button_lepas_rem.setEnabled(not self.control_is_enabled)

    # Jika dalam status berhenti karena dekat obyek
    # bisa lepas rem untuk menggerakkan kembali
    def lepas_rem(self):
        self.toggle_lepas_rem()
        if self.is_lepas_rem:
            QTimer.singleShot(5000, self.toggle_lepas_rem)
    
    def toggle_lepas_rem(self):
        self.is_lepas_rem = not self.is_lepas_rem
        self.toggle_controls()
    
def appExec():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    GPIO.cleanup()

def start_gui():
    sys.exit(appExec())

# if __name__ == "__main__":
    # start_gui()
    