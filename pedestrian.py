import numpy as np
import math
import cv2
cap = cv2.VideoCapture('TownCentreXVID.avi')
# fgbg = cv2.createBackgroundSubtractorMOG2(history=5, varThreshold=150)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=150, backgroundRatio=0.3)

def line1(x,y):
    return y - (29*x)/96.0 - 300

def line2(x,y):
    return y - (29*x)/96.0 - 500


crossedAbove = 0
crossedBelow = 0
points = set()
pointFromAbove = set()
pointFromBelow = set()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('pedestrianOutput.avi',fourcc, 25.0, (1920,1080))
font = cv2.FONT_HERSHEY_SIMPLEX
while(1):
    pointInMiddle = set()
    prev = points
    points = set()
    ret, frame = cap.read()
    fgmask = frame
    fgmask = cv2.blur(frame, (10,10))
    fgmask = fgbg.apply(fgmask)
    fgmask = cv2.medianBlur(fgmask, 7)
    oldFgmask = fgmask.copy()
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,1)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>40 and h>90:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2, lineType=cv2.LINE_AA)
            point = (int(x+w/2.0), int(y+h/2.0))
            points.add(point)
    for point in points:
        (xnew, ynew) = point
        if line1(xnew, ynew) > 0 and line2(xnew, ynew) < 0:
            pointInMiddle.add(point)
        for prevPoint in prev:
            (xold, yold) = prevPoint
            dist = cv2.sqrt((xnew-xold)*(xnew-xold)+(ynew-yold)*(ynew-yold))
            if dist[0] <= 120:
                if line1(xnew, ynew) >= 0 and line2(xnew, ynew) <= 0:
                    if line1(xold, yold) < 0: # Point entered from line above
                        pointFromAbove.add(point)
                    elif line2(xold, yold) > 0: # Point entered from line below
                        pointFromBelow.add(point)
                    else:   # Point was inside the block
                        if prevPoint in pointFromBelow:
                            pointFromBelow.remove(prevPoint)
                            pointFromBelow.add(point)

                        elif prevPoint in pointFromAbove:
                            pointFromAbove.remove(prevPoint)
                            pointFromAbove.add(point)

                if line1(xnew, ynew) < 0 and prevPoint in pointFromBelow: # Point is above the line
                    print('One Crossed Above')
                    print(point)
                    crossedAbove += 1
                    pointFromBelow.remove(prevPoint)

                if line2(xnew, ynew) > 0 and prevPoint in pointFromAbove: # Point is below the line
                    print('One Crossed Below')
                    print(point)
                    crossedBelow += 1
                    pointFromAbove.remove(prevPoint)


    for point in points:
        if point in pointFromBelow:
            cv2.circle(frame, point, 3, (255,0,255),6)
        elif point in pointFromAbove:
            cv2.circle(frame, point, 3, (0,255,255),6)
        else:
            cv2.circle(frame, point, 3, (0,0,255),6)
    cv2.line(frame, (0,300), (1920,880), (255, 0, 0), 4)
    cv2.line(frame, (0,500), (1920,1080), (255, 0, 0), 4)
    cv2.putText(frame,'People Going Above = '+str(crossedAbove),(1200,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'People Going Below = '+str(crossedBelow),(1200,100), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('a',oldFgmask)
    cv2.imshow('frame',frame)
    out.write(frame)
    l = cv2.waitKey(1) & 0xff
    if l == 27:
        break
cap.release()
cv2.destroyAllWindows()
