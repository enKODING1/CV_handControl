import cv2
import mediapipe as mp
import pyautogui as py

pos = py.position()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands



# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image,2), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        wrist = hand_landmarks.landmark[0]

        diff = int(abs(index.x - thumb.x)*100)
        if diff <= 3:
          py.moveTo(int(thumb.x*1000),int(thumb.y*1000))
        elif diff > 15:
          py.click()
          

        
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()