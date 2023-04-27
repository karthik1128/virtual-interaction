import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import gc

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=2)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = " "
keyboard = Controller()
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)                     # with Draw
    #hands = detector.findHands(img, draw=False)              #No Draw
    img = drawAll(img, buttonList)
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]                            # List of 21 Landmarks points
        bbox1 = hand1["bbox"]                                # Bounding Box info x, y, w, h
        centerPoint1 = hand1["center"]                       # center of the hand cx, cy
        handType1 = hand1["type"]                            # Hand TYpe Left or Right

        print(len(lmList1), lmList1)
        print(bbox1)
        print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)

        if len(hands)==2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]                            # List of 21 Landmarks points
            bbox2 = hand2["bbox"]                                # Bounding Box info x, y, w, h
            centerPoint2 = hand2["center"]                       # center of the hand cx, cy
            handType2 = hand2["type"]                            # Hand TYpe Left or Right

            fingers2 = detector.fingersUp(hand2)
            print(fingers1, fingers2)
            if lmList1:
              for button in buttonList:
                x, y = button.pos
                w, h = button.size
 
            if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)
 
                ## when clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.15)
 
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            
        

            
    cv2.imshow("Image", img)
    cv2.waitKey(1)