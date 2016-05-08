import numpy as np
import math
import cv2
cap = cv2.VideoCapture('TownCentreXVID.avi')
# fgbg = cv2.createBackgroundSubtractorMOG2(history=5, varThreshold=150)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=300)

i = 0
k = 0
crossedAbove = 0
crossedBelow = 0
points = set()
pointFromAbove = set()
pointFromBelow = set()
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
    # faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    if k%25 == 0:
        # print 'hello'
        # print w, h
        # cv2.imwrite('data/image'+str(i)+'.jpg', frame)
        i+=1
    k+=1
    oldFgmask = fgmask.copy()
    image, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,1)
    # # print a
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>40 and h>90:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2, lineType=cv2.LINE_AA)
            # print (int(x+w/2.0), int(y+h/2.0))
            # cv2.circle(frame, (int(x+w/2.0), int(y+h/2.0)), 3, (0,0,255),6)
            point = (int(x+w/2.0), int(y+h/2.0))
            points.add(point)
        # defects = cv2.convexityDefects(cnt,hull)
        # start = tuple(cnt[s][0])
        # end = tuple(cnt[e][0])
        # far = tuple(cnt[f][0])
        # cv2.line(frame,start,end,[0,255,0],2)
        # cv2.circle(frame,far,5,[0,0,255],-1)
    for point in points:
        (xnew, ynew) = point
        if (ynew - (29*xnew)/96.0 - 300) > 0 and (ynew - (29*xnew)/96.0 - 500) < 0:
            pointInMiddle.add(point)
        for prevPoint in prev:
            (xold, yold) = prevPoint
            dist = cv2.sqrt((xnew-xold)*(xnew-xold)+(ynew-yold)*(ynew-yold))
            # print point
            # print prevPoint
            if dist[0] <= 100:
                # print prevPoint
                # print point
                # print dist
                if ynew - (29*xnew)/96.0 - 300 > 0 and ynew - (29*xnew)/96.0 - 500 < 0:
                    if yold - (29*xold)/96.0 - 300 < 0: # Point entered from line above
                        pointFromAbove.add(point)
                    elif yold - (29*xold)/96.0 - 500 > 0: # Point entered from line below
                        pointFromBelow.add(point)
                        # print '=================='
                        # print 'Below Point Added'
                        # print point
                        # print '=================='
                    else:   # Point was inside the block
                        if prevPoint in pointFromBelow:
                            pointFromBelow.remove(prevPoint)
                            pointFromBelow.add(point)
                            # print '=================='
                            # print 'Below Point Updated'
                            # print point
                            # print '=================='

                        elif prevPoint in pointFromAbove:
                            pointFromAbove.remove(prevPoint)
                            pointFromAbove.add(point)

                if ynew - (29*xnew)/96.0 - 300 < 0 and prevPoint in pointFromBelow: # Point is above the line
                    print 'One Crossed Above'
                    print point
                    crossedAbove += 1
                    pointFromBelow.remove(prevPoint)

                if ynew - (29*xnew)/96.0 - 500 > 0 and prevPoint in pointFromAbove: # Point is below the line
                    print 'One Crossed Below'
                    print point
                    crossedBelow += 1
                    pointFromAbove.remove(prevPoint)


    for point in points:
        if point in pointFromBelow:
            cv2.circle(frame, point, 3, (255,0,255),6)
        elif point in pointFromAbove:
            cv2.circle(frame, point, 3, (0,255,255),6)
        else:
            cv2.circle(frame, point, 3, (0,0,255),6)
        # if point in pointInMiddle:
        #     cv2.circle(frame, point, 3, (255,0,255),6)
        # else:
        #     cv2.circle(frame, point, 3, (0,0,255),6)

    # if contours[1] is not None:
    #     x,y,w,h = cv2.boundingRect(contours[1])
    #     print x,y,w,h
    #     cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # for cont in a:

    #     if type(cont) == np.ndarray:
    #         x,y,w,h = cv2.boundingRect(cont)
    #         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #         # print tuple(cont)
    #         # cv2.rectangle(frame, tuple(cont[0][0][0]), tuple(cont[0][2][0]), (255,0,0), 2)
    cv2.line(frame, (0,300), (1920,880), (255, 0, 0), 4)
    cv2.line(frame, (0,500), (1920,1080), (255, 0, 0), 4)
    cv2.putText(frame,'People Crossed Above = '+str(crossedAbove),(1200,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'People Crossed Below = '+str(crossedBelow),(1200,100), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('frame',frame)
    l = cv2.waitKey(1) & 0xff
    if l == 27:
        break
cap.release()
cv2.destroyAllWindows()