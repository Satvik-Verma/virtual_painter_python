import cv2
import numpy as np
import time
import os
import hand_tracking_module as htm

brushThickness = 25
folderPath = "/Users/satvikverma/Downloads/Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[0]

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)

while True:
    # Import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)
    #print(lmList)

    if lmList is not None:
        # Tip of index and middle finger
        if len(lmList) > 8 and len(lmList) > 12:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            print(x1,y1)
            # Continue with further processing

        # Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        if fingers[1] and fingers[2]:
            # xp, yp = 0, 0
            print("Selection Mode")
            # # Checking for the click
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
 
        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

        

    # Setting the header image
    img[0:125, 0:1280] = header
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):  # Break the loop if 'q' is pressed
        break

cap.release()
cv2.destroyAllWindows()

