import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO
import concurrent.futures
import pygame
import time
import csv
from tkinter import messagebox
from datetime import datetime
import threading
import tkinter as tk
NO_FACE_THRESHOLD = 5  
no_face_start_time = None
EYE_CLOSED_DURATION_THRESHOLD = 10
eye_closed_start_time = None 
EAR_CONSEC_FRAMES = 20
NECK_CONSEC_FRAMES = 20
YOLO_DETECT_EVERY = 10
SOUND_INTERVAL = 1 
last_sound_time = 0  
ear_counter = 0
neck_counter = 0
frame_count = 0
last_yolo_results = []
last_log_time = time.time()  
LOG_INTERVAL = 5
yolo_model = YOLO('./database/best.pt')
pygame.mixer.init()
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

cap = cv2.VideoCapture(0)
def show_notification(message):
    def create_window():
        root = tk.Tk()
        root.overrideredirect(True)

        window_width = 300
        window_height = 100

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.configure(bg="lightyellow")

        label = tk.Label(root, text=message, font=("Arial", 12), bg="lightyellow", wraplength=280)
        label.pack(expand=True)

        root.after(5000, root.destroy)
        root.mainloop()

    threading.Thread(target=create_window).start()
def play_alert_sound(sound_file):
    global last_sound_time
    current_time = time.time()
    if current_time - last_sound_time >= SOUND_INTERVAL: 
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        last_sound_time = current_time

def calculate_ear(eye_landmarks):
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    return (A + B) / (2.0 * C)


def run_yolo(frame):
    small_frame = cv2.resize(frame, (256, 256))
    results = yolo_model.predict(source=small_frame, imgsz=256, conf=0.3, verbose=False)
    return results


def run_mediapipe(frame_rgb):
    results_pose = pose.process(frame_rgb)
    results_face = face_mesh.process(frame_rgb)
    return results_pose, results_face

def check_no_face_detected(results_face, frame):
    global no_face_start_time, last_log_time

    current_time = time.time()

    if not results_face.multi_face_landmarks:
        if no_face_start_time is None:
            no_face_start_time = current_time 
        elif current_time - no_face_start_time >= NO_FACE_THRESHOLD:
            show_notification("Không phát hiện khuôn mặt\nBạn hãy điều chỉnh tư thế ngồi giữa khung hình nhé.")
            play_alert_sound("./database/ting.mp3")

            if current_time - last_log_time >= LOG_INTERVAL:
                with open("./database/fatigue_log.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Không phát hiện khuôn mặt"])
                last_log_time = current_time
    else:
        no_face_start_time = None
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
future_yolo = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_count += 1
    cv2.putText(frame, f"An Q de thoat camera", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    future_mediapipe = executor.submit(run_mediapipe, frame_rgb)
    results_pose, results_face = future_mediapipe.result()
    check_no_face_detected(results_face, frame)
    flag_ear = False
    flag_yolo = False
    if results_pose.pose_landmarks:
        landmarks = results_pose.pose_landmarks.landmark
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        nose_x, nose_y = int(nose.x * w), int(nose.y * h)
        left_shoulder_x, left_shoulder_y = int(left_shoulder.x * w), int(left_shoulder.y * h)
        right_shoulder_x, right_shoulder_y = int(right_shoulder.x * w), int(right_shoulder.y * h)

        neck_x = (left_shoulder_x + right_shoulder_x) // 2
        neck_y = (left_shoulder_y + right_shoulder_y) // 2

        # Vẽ điểm
        # cv2.circle(frame, (nose_x, nose_y), 5, (255, 0, 0), -1)
        # cv2.circle(frame, (neck_x, neck_y), 5, (0, 0, 255), -1)

        # Tính khoảng cách theo phương Y giữa mũi và cổ (delta_y)
        delta_y = neck_y - nose_y 

        # Tính góc giữa mũi và cổ
        vector_x = nose_x - neck_x
        vector_y = neck_y - nose_y
        angle_rad = np.arctan2(vector_x, vector_y)
        angle_deg = np.abs(angle_rad * 180 / np.pi)

        cv2.putText(frame, f"Angle: {int(angle_deg)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Delta Y: {int(delta_y)}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        GUC_DAU_ANGLE = 45  
        GUC_DAU_DELTA_Y = 70 

        if delta_y < GUC_DAU_DELTA_Y:
            neck_counter += 1
        else:
            neck_counter = 0 

        if neck_counter >= NECK_CONSEC_FRAMES: 
            play_alert_sound("./database/ting.mp3")
            show_notification("GỤC ĐẦU\nBạn đang mệt mỏi!\nHãy tập thể dục hoặc ăn thức ăn theo gợi ý nhé.")
            current_time = time.time()
            if current_time - last_log_time >= LOG_INTERVAL:
                with open("./database/fatigue_log.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Gục đầu"])
                last_log_time = current_time

    if results_face.multi_face_landmarks:
        face_landmarks = results_face.multi_face_landmarks[0].landmark

        left_eye_idx = [33, 160, 158, 133, 153, 144]
        right_eye_idx = [362, 385, 387, 263, 373, 380]

        left_eye = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in left_eye_idx]
        right_eye = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in right_eye_idx]

        # for point in left_eye + right_eye:
        #     cv2.circle(frame, point, 2, (255, 0, 255), -1)

        avg_ear = (calculate_ear(left_eye) + calculate_ear(right_eye)) / 2
        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        ear_counter = ear_counter + 1 if avg_ear < 0.2 else 0
        if ear_counter >= EAR_CONSEC_FRAMES:
            play_alert_sound("./database/ting.mp3")
            show_notification("BUỒN NGỦ\nBạn đang mệt mỏi!\nHãy tập thể dục hoặc ăn thức ăn theo gợi ý nhé.")
            flag_ear = True
            if eye_closed_start_time is None:
                eye_closed_start_time = time.time()
            else:
                closed_duration = time.time() - eye_closed_start_time
                if closed_duration >= EYE_CLOSED_DURATION_THRESHOLD:
                    play_alert_sound("./database/ting.mp3")
                    show_notification("NGỦ GỤC\nBạn đang quá mệt mỏi!\nHãy nghỉ ngơi nhé.")
                    current_time = time.time()
                    if current_time - last_log_time >= LOG_INTERVAL:
                        with open("./database/fatigue_log.csv", "a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Ngủ gục"])
                        last_log_time = current_time
        else:
            eye_closed_start_time = None
    if frame_count % YOLO_DETECT_EVERY == 0:
        future_yolo = executor.submit(run_yolo, frame)

    if future_yolo and future_yolo.done():
        last_yolo_results = future_yolo.result()

    for result in last_yolo_results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0] * np.array([w / 256, h / 256, w / 256, h / 256]))
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = f"{yolo_model.names[class_id]} {confidence:.2f}"

            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
            # cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

            if "yawn" in label.lower():
                play_alert_sound("./database/ting.mp3")
                show_notification("NGÁP\nBạn đang mệt mỏi!\nHãy tập thể dục hoặc ăn thức ăn theo gợi ý nhé.")
                flag_yolo = True
                if flag_ear == True and flag_yolo == True:
                    current_time = time.time()
                    show_notification("NGÁP và BUỒN NGỦ\nBạn đang mệt mỏi!\nHãy tập thể dục hoặc ăn thức ăn theo gợi ý nhé.")
                    if current_time - last_log_time >= LOG_INTERVAL:
                        with open("./database/fatigue_log.csv", "a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Ngáp và buồn ngủ"])
                        last_log_time = current_time

    cv2.imshow("Phat Hien Met Moi Khi Hoc Online", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
executor.shutdown()
