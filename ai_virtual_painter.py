import cv2
import numpy as np
import time
import os
import hand_tracking_module as htm
 
#######################
brushThickness = 25
eraserThickness = 100

folderPath = "/Users/satvikverma/Downloads/Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    overlayList.append(image)
print(len(overlayList))
if overlayList:
    header = overlayList[0]
    drawColor = (255, 0, 255)
else:
    print("No valid images found in the folder.")
    header = None

# change the value to 0 or 1 to choose primary or secondary camera
    
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

max_failures = 10  # Maximum number of consecutive image capture failures allowed
consecutive_failures = 0  # Counter for consecutive failures


while True:
    # Import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)

    if lmList is not None: 
        # Tip of index and middle finger
        if len(lmList) > 8 and len(lmList) > 12:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            print(x1, y1)
            # Continue with further processing

        # Check which fingers are up
        fingers = detector.fingersUp()

        if len(fingers) > 2 and fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            # Checking for the click
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

        # If Drawing Mode - Index finger is up
        if len(fingers) > 1 and fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    if img is not None and imgInv is not None:
        # Resize imgInv to match the dimensions of img
        imgInv = cv2.resize(imgInv, (img.shape[1], img.shape[0]))

        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        if header is not None:
            img[0:125, 0:1280] = header

    # Setting the header image
    img[0:125, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Inv", imgInv)
    if cv2.waitKey(1) == ord('q'):  # Break the loop if 'q' is pressed
        break

cap.release()
cv2.destroyAllWindows()
########################
folderPath = "/Users/satvikverma/Desktop/Header"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
if overlayList:
    header = overlayList[0]
    drawColor = (255, 0, 255)
else:
    print("No valid images found in the folder.")
    header = None

 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
 
detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

max_failures = 10  # Maximum number of consecutive image capture failures allowed
consecutive_failures = 0  # Counter for consecutive failures
 
while True:
 
    # 1. Import image
    success, img = cap.read()

    if not success or img is None:
        continue  # Skip to the next iteration if image capture fails or img is None

    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
 
    if len(lmList) != 0:
 
        # print(lmList)
 
        # tip of index and middle fingers
       if len(lmList) > 8:
            x1, y1 = lmList[8][1:]
            
            if len(lmList) > 12:
                x2, y2 = lmList[12][1:]
 
        # 3. Check which fingers are up
                fingers = detector.fingersUp()
        # print(fingers)
 
        # 4. If Selection Mode - Two finger are up
                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    #print("Selection Mode")
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
                #print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
 
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
 
            # if drawColor == (0, 0, 0):
            #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
            #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            #
            # else:
            #     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
 
                xp, yp = x1, y1
 
 
        # # Clear Canvas when all fingers are up
        # if all (x >= 1 for x in fingers):
        #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)
 
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    if img is not None and imgInv is not None:
        # Resize imgInv to match the dimensions of img
        imgInv = cv2.resize(imgInv, (img.shape[1], img.shape[0]))

        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        if header is not None:
            img[0:125, 0:1280] = header


 
    # Setting the header image
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) == ord('q'):  # Break the loop if 'q' is pressed
        break

cap.release()
cv2.destroyAllWindows()
