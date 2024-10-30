import dlib
import cv2
import numpy as np

#==============================================================================
#   1. Fungsi konversi format landmarks
#       Input: landmarks dalam format dlib
#       Output: landmarks dalam format numpy
#==============================================================================          
def landmarks_to_np(landmarks, dtype="int"):
    # Mendapatkan jumlah landmarks
    num = landmarks.num_parts
    
    # Inisialisasi daftar koordinat (x, y)
    coords = np.zeros((num, 2), dtype=dtype)
    
    # Loop untuk 68 landmarks wajah dan mengonversinya
    # menjadi tuple (x, y)
    for i in range(0, num):
        coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
    # Mengembalikan daftar koordinat (x, y)
    return coords

#==============================================================================
#   ************************** Masuk ke fungsi utama **************************
#==============================================================================

predictor_path = "./data/shape_predictor_68_face_landmarks.dat"  # Jalur data pelatihan landmark wajah
detector = dlib.get_frontal_face_detector()  # Detektor wajah
predictor = dlib.shape_predictor(predictor_path)  # Detektor landmark wajah

cap = cv2.VideoCapture(0)

# Inisialisasi queue (antrian) untuk data time series
queue = np.zeros(30, dtype=int)
queue = queue.tolist()

while(cap.isOpened()):
    # Membaca frame video
    _, img = cap.read()
    
    # Konversi ke gambar grayscale (abu-abu)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Deteksi wajah
    rects = detector(gray, 1)
    
    # Operasi untuk setiap wajah yang terdeteksi
    for i, rect in enumerate(rects):
        # Mendapatkan koordinat
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y
        
        # Menggambar kotak di sekitar wajah, menambahkan label teks
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, "Wajah #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Deteksi landmarks        
        landmarks = predictor(gray, rect)
        landmarks = landmarks_to_np(landmarks)
        
        # Menandai landmarks pada wajah
        for (x, y) in landmarks:
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
     
        # Menghitung jarak Euclidean
        d1 = np.linalg.norm(landmarks[37] - landmarks[41])
        d2 = np.linalg.norm(landmarks[38] - landmarks[40])
        d3 = np.linalg.norm(landmarks[43] - landmarks[47])
        d4 = np.linalg.norm(landmarks[44] - landmarks[46])
        d_mean = (d1 + d2 + d3 + d4) / 4
        d5 = np.linalg.norm(landmarks[36] - landmarks[39])
        d6 = np.linalg.norm(landmarks[42] - landmarks[45])
        d_reference = (d5 + d6) / 2
        d_judge = d_mean / d_reference
        print(d_judge)
        
        # Penanda mata terbuka/tertutup berdasarkan threshold, mata tertutup flag=1, mata terbuka flag=0 (threshold dapat disesuaikan)
        flag = int(d_judge < 0.25)
        
        # Memasukkan flag ke dalam antrian
        queue = queue[1:len(queue)] + [flag]
        
        # Menentukan apakah lelah: jika lebih dari separuh elemen dalam antrian di bawah threshold
        if sum(queue) > len(queue) / 2:
            cv2.putText(img, "PERINGATAN!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(img, "AMAN", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Menampilkan hasil
    cv2.imshow("Hasil", img)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:  # Tekan "Esc" untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
