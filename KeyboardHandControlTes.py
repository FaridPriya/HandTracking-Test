import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import pydirectinput as pdi

#VARIABLES
########################################
wCam, hCam = 640, 480
pTime = 0
cTime = 0
########################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam) #set width camera, 3 adalah id dari width
cap.set(4, hCam) #set height camera, 4 adalah id dari height
detector = htm.handDetector(detectionCon=0.7) #detectionCon mengatur kecepatan deteksi koneksi di hand
while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.finddPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        
        #THUMB TIP
        ttX, ttY = lmList[4][1], lmList[4][2]
        cv2.circle(img, (ttX, ttY), 10, (255,0,255), cv2.FILLED)

        #INDEX FINGER TIP
        iftX, iftY = lmList[8][1], lmList[8][2]
        cv2.circle(img, (iftX, iftY), 10, (255,0,255), cv2.FILLED)

        #MIDDLE FINGER TIP
        mftX, mftY = lmList[12][1], lmList[12][2]
        cv2.circle(img, (mftX, mftY), 10, (255,0,255), cv2.FILLED)

        #LINE
        cv2.line(img, (ttX,ttY), (iftX,iftY), (255, 0, 255), 3) # gambar garis antara pont 8 dan 4
        cv2.line(img, (ttX,ttY), (mftX,mftY), (255, 0, 255), 3) # gambar garis antara pont 12 dan 4
        

        lengthIndexThumb = int(math.hypot(iftX - ttX, iftY - ttY)) #cari jarak antara 2 titik (point 8 dan 4)
        lengthMidleThumb = int(math.hypot(mftX - ttX, mftY - ttY)) #cari jarak antara 2 titik (point 8 dan 4)
        #print(lengthIndexThumb)

        #hand range 15 - 140 (di tutuorial 50 - 300)
        #volume range -65 - 0
        #vol = np.interp(length, [0, 25], [0, 1])
        #print(f"length = {int(length)}, vol = {vol}")

        if lengthIndexThumb < 15:
            pdi.keyDown('w')
        if lengthMidleThumb < 15:
            pdi.keyDown('a')

    #FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1) #buat ngatur delay