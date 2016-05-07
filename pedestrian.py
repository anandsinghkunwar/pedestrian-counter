import numpy as np
import cv2
cap = cv2.VideoCapture('TownCentreXVID.avi')
# fgbg = cv2.createBackgroundSubtractorMOG2(history=5, varThreshold=150)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=300)

i = 0
k = 0
points = set()
while(1):
    prev = points
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
    for a in contours:
        x,y,w,h = cv2.boundingRect(a)
        if w>40 and h>90:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2, lineType=cv2.LINE_AA)
            print (int(x+w/2.0), int(y+h/2.0))
            cv2.circle(frame, (int(x+w/2.0), int(y+h/2.0)), 3, (0,0,255),6)
            points.add((int(x+w/2.0), int(y+h/2.0)))
        # defects = cv2.convexityDefects(cnt,hull)
        # start = tuple(cnt[s][0])
        # end = tuple(cnt[e][0])
        # far = tuple(cnt[f][0])
        # cv2.line(frame,start,end,[0,255,0],2)
        # cv2.circle(frame,far,5,[0,0,255],-1)


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
    # cv2.clipLine(frame, (1,1), (20,20))
    cv2.imshow('frame',frame)
    l = cv2.waitKey(1) & 0xff
    if l == 27:
        break
cap.release()
cv2.destroyAllWindows()