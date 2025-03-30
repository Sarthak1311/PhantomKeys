import mediapipe as mp 
import cv2
import math 
import numpy as np 
import os
import time  


def calcDist(idx_x, idx_y, thumb_x, thumb_y):
    return math.sqrt((idx_x - thumb_x)**2 + (thumb_y - idx_y)**2)


def mapDist2Vol(dist):
    return np.interp(dist, [10, 320], [0, 100])  


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


mphands = mp.solutions.hands
hands = mphands.Hands()
mpdrawing = mp.solutions.drawing_utils

last_volume = 50  
last_detected_time = time.time()  # Store last hand detection time
timeout = 2  # 2 seconds timeout before muting

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    volume = last_volume 

    if result.multi_hand_landmarks:
        for hndlm in result.multi_hand_landmarks:
            mpdrawing.draw_landmarks(frame, hndlm, mphands.HAND_CONNECTIONS)

            # Get coordinates
            thumb_tip = hndlm.landmark[4]
            idx_tip = hndlm.landmark[8]
            h, w, _ = frame.shape
            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(idx_tip.x * w), int(idx_tip.y * h)

            # Calculate distance and map to volume
            dist = calcDist(x2, y2, x1, y1)
            volume = mapDist2Vol(dist)

            # Update last detected time
            last_detected_time = time.time()

    # 🔹 If no hand is detected for 2 seconds, keep the last volume
    if time.time() - last_detected_time > timeout:
        volume = last_volume  


    os.system(f"osascript -e 'set volume output volume {int(volume)}'")
    last_volume = volume 

    # 🔹 Display volume level on screen
    cv2.putText(frame, f"Volume: {int(volume)}%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


    cv2.imshow("Camera", frame)

    # Exit when 'ESC' is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
