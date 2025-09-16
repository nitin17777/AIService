import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def analyze_pushups(uploaded_file):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    cap = cv2.VideoCapture(temp_path)
    counter = 0
    stage = None
    quality_feedback = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 160:
                    stage = 'up'
                if angle < 90 and stage == 'up':
                    stage = 'down'
                    counter += 1

                if angle < 70:
                    quality_feedback.append("Go lower for better form")
                elif angle > 170:
                    quality_feedback.append("Fully extend arms")

    cap.release()
    # Delete temp file after use
    os.remove(temp_path)

    return {
        "exercise": "pushups",
        "count": counter,
        "feedback_sample": quality_feedback[:5]
    }
