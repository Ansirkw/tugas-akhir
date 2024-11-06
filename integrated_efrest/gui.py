import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel
import cv2 as cv
import dlib
import numpy as np
import motor

motor.maju()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.cap = cv.VideoCapture(0)  # Use 0 for the default camera
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
        
    def update_frame(self):
        def landmarks_to_np(landmarks, dtype="int"):
            
            num = landmarks.num_parts
            
            # initialize the list of (x, y)-coordinates
            coords = np.zeros((num, 2), dtype=dtype)
            
            # loop over the 68 facial landmarks and convert them
            # to a 2-tuple of (x, y)-coordinates
            for i in range(0, num):
                coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
            # return the list of (x, y)-coordinates
            return coords
        
        predictor_path = "./driver-fatigue-monitoring-system/data/shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(predictor_path)
        # Capture frame-by-frame

        queue = np.zeros(30,dtype=int)
        queue = queue.tolist()

        while(self.cap.isOpened()):
            _, img = self.cap.read()
            
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            
            rects = detector(gray, 1)
            
            for i, rect in enumerate(rects):
                x = rect.left()
                y = rect.top()
                w = rect.right() - x
                h = rect.bottom() - y
                
                cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                cv.putText(img, "Face #{}".format(i + 1), (x - 10, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv.LINE_AA)
                
                landmarks = predictor(gray, rect)
                landmarks = landmarks_to_np(landmarks)

                for (x, y) in landmarks:
                    cv.circle(img, (x, y), 2, (0, 0, 255), -1)
            
                d1 =  np.linalg.norm(landmarks[37]-landmarks[41])
                d2 =  np.linalg.norm(landmarks[38]-landmarks[40])
                d3 =  np.linalg.norm(landmarks[43]-landmarks[47])
                d4 =  np.linalg.norm(landmarks[44]-landmarks[46])
                d_mean = (d1+d2+d3+d4)/4
                d5 =np.linalg.norm(landmarks[36]-landmarks[39])
                d6 =np.linalg.norm(landmarks[42]-landmarks[45])
                d_reference = (d5+d6)/2
                d_judge = d_mean/d_reference
                print(d_judge)
                
                flag = int(d_judge<0.25)
                
                queue = queue[1:len(queue)] + [flag]
                
                if sum(queue) > len(queue)/2 :
                    cv.putText(img, "WARNING !", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv.LINE_AA)
                    self.status_label.setText("Limited")
                else:
                    cv.putText(img, "SAFE", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv.LINE_AA)
                    self.status_label.setText("Normal")
            
            k = cv.waitKey(5) & 0xFF
            if k==27:
                break

            # Get the image dimensions
            height, width, channel = img.shape
            bytes_per_line = 3 * width

            # Convert the OpenCV image to QImage
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # Set the QImage in the QLabel
            self.image_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.image_label.size(), Qt.KeepAspectRatio))



if __name__ == "__main__":
# Main execution
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    app.exec_()

