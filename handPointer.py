import numpy as np
import mediapipe as mp
import cv2
import pyautogui as pya
import math

# Initialize Mediapipe Hand Tracking
mphands = mp.solutions.hands
hands = mphands.Hands()
mpDrawing = mp.solutions.drawing_utils

# Get screen size
screen_w, screen_h = pya.size()

# Start Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    imgrgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(imgrgb)

    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            mpDrawing.draw_landmarks(frame, handlm, mphands.HAND_CONNECTIONS)

            # Get Index and Middle Finger Tip Coordinates
            h, w, _ = frame.shape
            idx_tip = handlm.landmark[8]
            middle_tip = handlm.landmark[12]
            thumb_tip =handlm.landmark[4]

            x1, y1 = int(idx_tip.x * w), int(idx_tip.y * h)
            x2, y2 = int(middle_tip.x * w), int(middle_tip.y * h)
            x3, y3 = int (thumb_tip.x * w), int(thumb_tip.y * h)

            # Map Hand Position to Screen
            screen_x = np.interp(x1, [0, w], [0, screen_w])
            screen_y = np.interp(y1, [0, h], [0, screen_h])

            pya.moveTo(screen_x, screen_y)

            if math.dist([x1, y1], [x2, y2]) < 20:  # Using Euclidean distance
                pya.click()
                cv2.putText(frame, "Click", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Right Click Gesture (Thumb & Index Finger Pinch)
            if math.dist([x1, y1], [x3, y3]) < 20:  # Adjusted sensitivity
                pya.rightClick()
                cv2.putText(frame, "Double Click", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Drag Gesture (Thumb, Index, & Middle Finger Pinch)
            if math.dist([x1, y1], [x3, y3]) < 20 and math.dist([x2, y2], [x3, y3]) < 20:
                pya.mouseDown()
                cv2.putText(frame, "Drag", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                pya.mouseUp()

            


    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
