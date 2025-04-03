import mediapipe as mp
import os
import cv2
import numpy as np
import pygame

#create mediapipe object
mphands = mp.solutions.hands()
hands= mphands.Hands()
mp_drawing= mp.solutions.drawing_utils()

cap= cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    #flip and convert the frame 
    frame = cv2.flip(frame,1)
    imgrgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    result = hands.process(imgrgb)

    if result.mutli_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,handlms,mphands.HAND_CONNECTIONS)

            # getting the frame size
            w,h,_ = frame.shape
            # getting the coordinates of the fingers 
            thumb_tip = handlms.landmark[4]
            index_tip = handlms.landmark[8]
            middle_tip = handlms.landmark[12]
            ring_tip = handlms.landmark[16]
            pinky_tip = handlms.landmark[20]

