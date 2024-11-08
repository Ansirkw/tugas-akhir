from RPi import GPIO
import time 
from PyQt5.QtCore import QThread, pyqtSignal
from pin_config import PINS
import cv2
import dlib
import numpy as np

class SleepyDetectorThread(QThread):
    data_sleepy_detector = pyqtSignal(tuple)

    def run(self):
        predictor_path = "./data/shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(predictor_path)
        cap = cv2.VideoCapture(0)
        while True:
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)
            sleepy_warning = False

            for rect in rects:
                landmarks = predictor(gray, rect)
                landmarks = self.landmarks_to_np(landmarks)
                d1 = np.linalg.norm(landmarks[37] - landmarks[41])
                d2 = np.linalg.norm(landmarks[38] - landmarks[40])
                d3 = np.linalg.norm(landmarks[43] - landmarks[47])
                d4 = np.linalg.norm(landmarks[44] - landmarks[46])
                d_mean = (d1 + d2 + d3 + d4) / 4
                d5 = np.linalg.norm(landmarks[36] - landmarks[39])
                d6 = np.linalg.norm(landmarks[42] - landmarks[45])
                d_reference = (d5 + d6) / 2
                d_judge = d_mean / d_reference

                flag = int(d_judge < 0.25)
                queue = queue[1:len(queue)] + [flag]

                if sum(queue) > len(queue) / 2:
                    sleepy_warning = True
                    cv2.putText(img, "PERINGATAN!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, "SAFE", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
            
            self.data_sleepy_detector.emit((img, sleepy_warning))

    def landmarks_to_np(landmarks, dtype="int"):
        num = landmarks.num_parts
        coords = np.zeros((num, 2), dtype=dtype)
        for i in range(0, num):
            coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
        return coords