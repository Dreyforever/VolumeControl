import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Enabling the camera
cap = cv2.VideoCapture(0)
cTime = 0
pTime = 0

# defining the detector that will be used for hand detection
detector = htm.HandDetector(detectionCon=0.7)

# Establishing connection with the system's audio devices
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

range = volume.GetVolumeRange()

# defining the volune ranges
Volmin = range[0]
Volmax = range[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        
        # finding the coordinates of the tip of the thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # drawing a cirle around the above points and a line connecting the two
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2),(255,0,255),3)

        # Finding the distance between the two points
        length = math.hypot(x2-x1, y2-y1)
        # Range of length is 15 - 225 

        # Mapping the length range with the volume range
        vol = np.interp(length,[15,225],[Volmin, Volmax])
        print(vol)

        # Using vol to set the sound level of the system's audio device
        volume.SetMasterVolumeLevel(vol, None)

    # Calculating fps of the video feed and printing it on the video
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
