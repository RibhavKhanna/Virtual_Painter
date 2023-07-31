import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2):
        self.mode=mode
        self.maxHands=maxHands
        # self.detectionCon=detectionCon
        # self.trackCon=trackCon
        

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def findHandds(self,frame,draw=True):
        imgRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)

        return frame        

    def findPosition(self,frame,handNo=0,draw=True):
        self.lmList=[]

        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv.circle(frame,(cx,cy),10,(255,0,255),cv.FILLED)
        
        return self.lmList
    
    def fingersUp(self):
        fingers=[]

        # Thumb
        if self.lmList[self.tipIds[0]][1]<self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
         # 4 fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    
def main():
    pTime=0
    cTime=0
    cap=cv.VideoCapture(0)
    detector=handDetector()
    while True:
        sucess,frame=cap.read()
        frame=detector.findHandds(frame)
        lmList=detector.findPosition(frame)
        # if len(lmList)!=0:
        #     print(lmList[4])

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        if sucess:
            cv.imshow("hand",frame)
    
        cv.waitKey(1)



if __name__=="__main__":
    main()