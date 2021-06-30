import cv2
import mediapipe
import pyautogui as py

pos = py.position()
    
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
 
capture = cv2.VideoCapture(0) #내 노트북 캠에 연결을 한다

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1500)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
capture.set(cv2.CAP_PROP_FPS, 25)

with handsModule.Hands(
    static_image_mode=False,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8, 
    max_num_hands=1) as hands:
 
    while (True):
 
        ret,frame = capture.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
 
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                thumb = handLandmarks.landmark[4]
                index = handLandmarks.landmark[8]
                wrist = handLandmarks.landmark[0]

                diff = int(abs(index.x - thumb.x)*100)
                print(diff)
                if diff <= 3:
                    py.moveTo(thumb.x*1000,thumb.y*1000)
                elif diff >= 12:
                    py.click()


        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
cv2.destroyAllWindows()
capture.release()