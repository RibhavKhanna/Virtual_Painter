import cv2 as cv
import numpy as np
import mediapipe as mp
import os
import HandTrackingModule as htm
import imutils

folderPath="Header"
myList=os.listdir(folderPath)
# print(myList)
overlayList=[]
for imPath in myList:
    image=cv.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header=overlayList[0]
drawColor=(255,0,255)
brushThickness=15
xp,yp=0,0

cap=cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector=htm.handDetector()

imgCanvas=np.zeros((960,1280,3),np.uint8)

while True:
    sucess,img=cap.read()
    img = imutils.resize(img, width=1280,height=720)
    img=cv.flip(img,1)
    
    # find landmarks
    img=detector.findHandds(img)
    lmList=detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        x1,y1=lmList[8][1:] # tip of index finger
        x2,y2=lmList[12][1:] # tip of middle finger


        # check which fingers are up
        fingers=detector.fingersUp()#  # 0 is for up 1 for down
        # print(fingers)

        

        # selection mode when 2 fingers are up
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            if y1<141:
                if 250<x1<450:
                    header=overlayList[0]
                    drawColor=(255,0,255)
                elif 550<x1<750:
                    header=overlayList[1]
                    drawColor=(255,0,0)
                elif 800<x1<950:
                    header=overlayList[2]
                    drawColor=(0,255,0)
                elif 1050<x1<1209:
                    header=overlayList[3]
                    drawColor=(0,0,0)    
            cv.rectangle(img,(x1,y1-5),(x2,y2+5),drawColor,cv.FILLED)
            # print("selection mode")
        # if drawing mode-> Index finger is up
        if fingers[1] and fingers[2]==False:
            cv.circle(img,(x1,y1),20,drawColor,cv.FILLED)
            # print("drawing mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            
            if drawColor==(0,0,0):
                cv.line(img,(xp,yp),(x1,y1),drawColor,brushThickness+85)
                cv.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness+85)
            else:
                cv.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp=x1,y1
    
    
    imgGray=cv.cvtColor(imgCanvas,cv.COLOR_BGR2GRAY)
    _,imgInv=cv.threshold(imgGray,50,255,cv.THRESH_BINARY_INV)

    imgInv=cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR)
    img=cv.bitwise_and(img,imgInv)
    img=cv.bitwise_or(img,imgCanvas)
    
    # setting the header img
    img[0:141,0:1280]=header

    # img=cv.addWeighted(img,0.5,imgCanvas,0.5,0)
   
    if sucess:
            cv.imshow("Virtual painter",img)
            # cv.imshow("Virtual painter",imgCanvas)
    
    cv.waitKey(1)

