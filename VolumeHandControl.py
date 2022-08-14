import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#VARIABLES
########################################
wCam, hCam = 640, 480
pTime = 0
cTime = 0
########################################


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

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
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 #cari titik tengah di garid antara point hand 8 dan 4

        cv2.circle(img, (x1, y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3) # gambar garis antara pont 8 dan 4
        cv2.circle(img, (cx, cy), 10, (255,0,255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1) #cari jarak antara 2 titik (point 8 dan 4)
        #print(length)

        #hand range 15 - 140 (di tutuorial 50 - 300)
        #volume range -65 - 0
        vol = np.interp(length, [15, 140], [minVol, maxVol])
        print(f"length = {int(length)}, vol = {vol}")
        volume.SetMasterVolumeLevel(vol, None)

        if length < 15:
            cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)

    #FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1) #buat ngatur delay