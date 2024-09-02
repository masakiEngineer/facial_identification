import cv2
import mediapipe as mp
from fer import FER
from deepface import DeepFace
import time
import tkinter as tk
from tkinter import ttk
import threading

# Tkinter の初期化
root = tk.Tk()
root.title("表示オプション")

# 表示オプションの初期値
display_options = {
    "points": tk.IntVar(value=0),
    "text": tk.IntVar(value=0),
    "emotion": tk.IntVar(value=0),
    "bbox": tk.IntVar(value=0),
    "demographics": tk.IntVar(value=0),
}

# 表示切替用ラジオボタンの作成
ttk.Label(root, text="顔の特徴検出:").pack(anchor="w")
ttk.Radiobutton(root, text="ON", variable=display_options["points"], value=1).pack(anchor="w")
ttk.Radiobutton(root, text="OFF", variable=display_options["points"], value=0).pack(anchor="w")

ttk.Label(root, text="口/目の変化検出:").pack(anchor="w")
ttk.Radiobutton(root, text="ON", variable=display_options["text"], value=1).pack(anchor="w")
ttk.Radiobutton(root, text="OFF", variable=display_options["text"], value=0).pack(anchor="w")

ttk.Label(root, text="感情検出:").pack(anchor="w")
ttk.Radiobutton(root, text="ON", variable=display_options["emotion"], value=1).pack(anchor="w")
ttk.Radiobutton(root, text="OFF", variable=display_options["emotion"], value=0).pack(anchor="w")

ttk.Label(root, text="BBOXの表示:").pack(anchor="w")
ttk.Radiobutton(root, text="ON", variable=display_options["bbox"], value=1).pack(anchor="w")
ttk.Radiobutton(root, text="OFF", variable=display_options["bbox"], value=0).pack(anchor="w")

# ttk.Label(root, text="性別と年齢予測:").pack(anchor="w")
# ttk.Radiobutton(root, text="ON", variable=display_options["demographics"], value=1).pack(anchor="w")
# ttk.Radiobutton(root, text="OFF", variable=display_options["demographics"], value=0).pack(anchor="w")

# Mediapipe の初期化
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# FER の初期化
emotion_detector = FER()

# カメラからのビデオキャプチャを開始
cap = cv2.VideoCapture(0)

# 目が閉じている時間の計測用
eyes_closed_start_time = None
eyes_closed_duration = 3  # 秒
eyes_closed_flag = False

def is_mouth_open(landmarks):
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]
    lip_distance = lower_lip.y - upper_lip.y
    return lip_distance > 0.03

def are_eyes_closed(landmarks):
    left_eye_upper = landmarks[159]
    left_eye_lower = landmarks[145]
    right_eye_upper = landmarks[386]
    right_eye_lower = landmarks[374]
    
    left_eye_distance = left_eye_lower.y - left_eye_upper.y
    right_eye_distance = right_eye_lower.y - right_eye_upper.y
    
    return left_eye_distance < 0.02 and right_eye_distance < 0.02

def update_display():
    global eyes_closed_start_time, eyes_closed_flag

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # フレームを反転（鏡像）
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        # 顔のランドマークを検出
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        # 表情を認識
        emotion, score = emotion_detector.top_emotion(frame)

        # 性別や年齢を認識
        demographics = None
        if display_options["demographics"].get() == 1:
            try:
                analysis = DeepFace.analyze(frame, actions=['age', 'gender'], enforce_detection=False)
                demographics = f"{analysis['gender']}, {int(analysis['age'])} years"
            except Exception as e:
                demographics = "Error in prediction"

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                
                # 緑の点の表示
                if display_options["points"].get() == 1:
                    for idx, landmark in enumerate(landmarks):
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                
                # BBOXの表示
                if display_options["bbox"].get() == 1:
                    x_min = min([int(landmark.x * w) for landmark in landmarks])
                    y_min = min([int(landmark.y * h) for landmark in landmarks])
                    x_max = max([int(landmark.x * w) for landmark in landmarks])
                    y_max = max([int(landmark.y * h) for landmark in landmarks])
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 255), 2)

                # Face:XXの表示
                if display_options["emotion"].get() == 1 and emotion:
                    emotion_text = f"Face: {emotion.capitalize()}"
                    cv2.putText(frame, emotion_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                # mouth, eyes, sleepingの表示
                if display_options["text"].get() == 1:
                    if is_mouth_open(landmarks):
                        cv2.putText(frame, "Mouth is open", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    if are_eyes_closed(landmarks):
                        if eyes_closed_start_time is None:
                            eyes_closed_start_time = time.time()
                        else:
                            elapsed_time = time.time() - eyes_closed_start_time
                            if elapsed_time > eyes_closed_duration:
                                eyes_closed_flag = True
                    else:
                        eyes_closed_start_time = None
                        eyes_closed_flag = False

                    if eyes_closed_flag:
                        cv2.putText(frame, "Sleeping!", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    elif are_eyes_closed(landmarks):
                        cv2.putText(frame, "Eyes are closed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # 性別と年齢の表示
                if demographics:
                    cv2.putText(frame, demographics, (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # 結果を表示
        cv2.imshow('Face Tracking with Emotion and Demographics Detection', frame)

        # 'q'キーが押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # リソースを解放
    cap.release()
    cv2.destroyAllWindows()

# OpenCVの処理を別スレッドで実行
opencv_thread = threading.Thread(target=update_display)
opencv_thread.daemon = True
opencv_thread.start()

# Tkinterのメインループを開始
root.mainloop()