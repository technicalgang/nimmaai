import cv2
import numpy as np
import time
import os
import modules.HandTrackingModule as htm
################
brushthick=15
erthick=50
#################
d = os.path.dirname(__file__)
folder=d+"\Header"
myList=os.listdir(folder)
print(myList)
overlay=[]

for imPath in myList:# taking the images and adding it to the list
    image=cv2.imread(f'{folder}/{imPath}')
    overlay.append(image)
print(len(overlay))
header=overlay[0]
drawColor= (255,0,255)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=1)
xp,yp=0,0
imgcanvas=np.zeros((720,1280,3),np.uint8)
while True:
    #1. import the images
    success, img = cap.read()
    img=cv2.flip(img,1)

    #2. Hand lankmarks
    img = detector.findHands(img)
    limlist=detector.findPosition(img,draw=False)
    if len(limlist)!=0:
        #print(limlist)
        x1,y1=limlist[8][1:]#FOR TIP of INDEX FINGER
        x2,y2=limlist[12][1:]#for tip of middle finger

        #3. Check which fingers are up(1=paint,2=Select)
        fingers=detector.fingersUp()
        #print(fingers)

        #4. if selection = 2 fingerws are up we have to selection
        if fingers[1] and fingers[2]:

            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
            xp,yp=0,0
            #print("selection")
            if y1<120:
                if 0<x1<200:#When yoy touch the logo you exit
                    exit()
                if 250<x1<350:
                    header=overlay[0]
                    drawColor=(255,0,255)#pink
                elif 400<x1<650:
                    header=overlay[1]
                    drawColor=(255,0,0)#blue
                elif 700<x1<950:
                    header=overlay[2]
                    drawColor=(0,255,0)#green
                elif 1050<x1<1200:
                    header=overlay[3]
                    drawColor=(0,0,0)#black
        #5. Drawing mode if index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            #print("Draw")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,erthick)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,erthick)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushthick)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,brushthick)
            xp,yp=x1,y1

    #TO MAKE SURE THAT THE IMAGE WITHOUT OPACITY ADDING IT TOGATHJER

    imgGray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgcanvas)
    img[0:120,0:1280]=header#size of the image{header image}
    #img=cv2.addWeighted(img,0.5,imgcanvas,0.5,0)
    cv2.imshow("Painter",img)
    cv2.imshow("Painter-started",imgcanvas)
    cv2.waitKey(1)
