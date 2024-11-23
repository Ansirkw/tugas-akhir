import RPi.GPIO as GPIO
import time

# Konfigurasi GPIO
BUZZER_PIN = 18  # Pin GPIO yang digunakan

GPIO.setmode(GPIO.BCM)  # Menggunakan penomoran GPIO
GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Mengatur pin sebagai output

try:
    print("Tes buzzer dimulai...")
    for i in range(5):  # Bunyi buzzer 5 kali
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Aktifkan buzzer
        time.sleep(0.5)  # Durasi buzzer menyala (0.5 detik)
        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Matikan buzzer
        time.sleep(0.5)  # Jeda sebelum buzzer berbunyi lagi
    print("Tes buzzer selesai.")
except KeyboardInterrupt:
    print("Tes dihentikan oleh pengguna.")
finally:
    GPIO.cleanup()  # Reset semua konfigurasi GPIO
