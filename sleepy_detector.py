import RPi.GPIO as GPIO
import time
import dlib
import cv2
import numpy as np

# =================== Setup Pin GPIO ===================
# Setup motor DC
in1 = 15
in2 = 18
en_a = 6
in3 = 8
in4 = 7
en_b = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en_b, GPIO.OUT)

motor_a = GPIO.PWM(en_a, 100)
motor_b = GPIO.PWM(en_b, 100)
motor_a.start(75)
motor_b.start(75)

# Setup buzzer
buzzer_pin = 18
GPIO.setup(buzzer_pin, GPIO.OUT)

# Setup sensor ultrasonik
trigger_pin_1 = 20
echo_pin_1 = 16
trigger_pin_2 = 26
echo_pin_2 = 19

GPIO.setup(trigger_pin_1, GPIO.OUT)
GPIO.setup(echo_pin_1, GPIO.IN)
GPIO.setup(trigger_pin_2, GPIO.OUT)
GPIO.setup(echo_pin_2, GPIO.IN)

# =================== Sleepy Detector Setup ===================
def landmarks_to_np(landmarks, dtype="int"):
    num = landmarks.num_parts
    coords = np.zeros((num, 2), dtype=dtype)
    for i in range(0, num):
        coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
    return coords

predictor_path = "./data/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

cap = cv2.VideoCapture(0)
queue = np.zeros(30, dtype=int).tolist()

# =================== Function Definitions ===================
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

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, False)
        time.sleep(delay)

def set_motor_speed(speed_percentage):
    motor_a.ChangeDutyCycle(speed_percentage)
    motor_b.ChangeDutyCycle(speed_percentage)

# Fungsi untuk menggerakkan motor maju, mundur, belok kiri, belok kanan, dan berhenti
def motor_forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    print("Maju")

def motor_backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    print("Mundur")

def motor_left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    print("Belok Kiri")

def motor_right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    print("Belok Kanan")

def motor_stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    print("Stop")

# =================== Main Loop ===================
try:
    while True:
        # =================== Ultrasonik Detection ===================
        distance_1 = get_distance(trigger_pin_1, echo_pin_1)
        distance_2 = get_distance(trigger_pin_2, echo_pin_2)
        status_1 = get_status(distance_1)
        status_2 = get_status(distance_2)

        # =================== Sleepy Detection ===================
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        sleepy_warning = False

        for rect in rects:
            landmarks = predictor(gray, rect)
            landmarks = landmarks_to_np(landmarks)
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

        # =================== Motor and Buzzer Control ===================
        if status_1 == "PERINGATAN!" or status_2 == "PERINGATAN!":
            # Jika ada peringatan dari ultrasonik, hentikan motor
            motor_stop()
            print("Motor Stopped due to Ultrasonic Warning!")
        elif sleepy_warning:
            # Jika ada peringatan dari sleepy detector, perlambat motor dan nyalakan buzzer
            set_motor_speed(37.5)  # Setengah dari kecepatan motor
            buzz(1000, 0.5)  # Bunyi buzzer
            print("Sleepy Warning! Motor Speed Reduced and Buzzer Activated!")
        else:
            # Kontrol motor berdasarkan input keyboard
            user_input = input("Masukkan perintah (w/a/s/d/c): ")
            if user_input == 'w':
                motor_forward()
            elif user_input == 's':
                motor_backward()
            elif user_input == 'a':
                motor_left()
            elif user_input == 'd':
                motor_right()
            elif user_input == 'c':
                motor_stop()

        # Delay agar pembacaan sensor lebih stabil
        time.sleep(1)

except KeyboardInterrupt:
    print("Program dihentikan")
finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
