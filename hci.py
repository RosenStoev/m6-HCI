import os
import cv2
import mediapipe as mp
import numpy as np
import math


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

avet = 0
avek = 0
aveh = 0
i = 0


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image.flags.writeable = False
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

        try:
            if i <= 5:
                left_thumb = results.pose_landmarks.landmark[31]
                left_ankle = results.pose_landmarks.landmark[27]
                left_knee = results.pose_landmarks.landmark[25]
                left_hip = results.pose_landmarks.landmark[23]
                left_shoulder = results.pose_landmarks.landmark[11]

                left_tib_ang = abs(math.degrees(math.atan2((left_knee.x - left_ankle.x), (left_knee.y - left_ankle.y))) - math.degrees(math.atan2((left_ankle.x - left_thumb.x), (left_ankle.y - left_thumb.y)))) - 90
                left_knee_ang = abs(math.degrees(math.atan2((left_hip.x - left_knee.x), (left_hip.y - left_knee.y))) - math.degrees(math.atan2((left_knee.x - left_ankle.x), (left_knee.y - left_ankle.y)))) - 90
                left_hip_ang = abs(math.degrees(math.atan2((left_shoulder.x - left_hip.x), (left_shoulder.y - left_hip.y))) - math.degrees(math.atan2((left_hip.x - left_knee.x), (left_hip.y - left_knee.y)))) - 90

                avet = avet + left_tib_ang
                avek = avek + left_knee_ang
                aveh = aveh + left_hip_ang

                i = i + 1
            else:
                os.system('cls')
                print((avet/i, avek/i, aveh/i))
                i = 1
                avet = 0
                avek = 0
                aveh = 0
        except:
            z = 1

        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
cap.release()
cv2.destroyAllWindows()