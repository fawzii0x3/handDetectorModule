import cv2
import numpy as np
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False , hands = 2 , complexity = 1 , detect = 0.5 , track = 0.5):
        #making setup var
        self.static_mode = mode
        self.max_hands = hands
        self.model_complexity = complexity
        self.detection_confi = detect
        self.tracking_confi  = track
        #setting up the mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_mode,self.max_hands,self.model_complexity,self.detection_confi,self.tracking_confi)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if draw:
            if self.results.multi_hand_landmarks :
                for handLms in self.results.multi_hand_landmarks :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo = 0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[8])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()