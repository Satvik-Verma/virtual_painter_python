import cv2
import numpy as np
import time
import os
from hand_tracking_module import HandDetector

folderPath = "/Users/satvikverma/Downloads/Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    if image is not None:
        overlayList.append(image)
    else:
        print(f"Failed to read image: {impath}")
print(len(overlayList))

if len(overlayList) > 0:
    header = overlayList[0]
else:
    print("No valid header image found.")

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.85)

while True:
    # Import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.findHands(img)
    
    # Check which fingers are up
    # If selection mode - two fingers up, then select not draw
    # If drawing mode - index finger up, only draw

    # Setting the header image
    if header is not None:
        img[0:125, 0:1280] = header

    cv2.imshow("Image", img)
    cv2.waitKey(1)
