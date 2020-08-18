# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import cv2
import numpy as np
import math

img_out1 = np.zeros((540,960),dtype=np.uint8)
img_out2 = np.zeros((540,960),dtype=np.uint8)
img_out3 = np.zeros((540,960),dtype=np.uint8)

cap = cv2.VideoCapture('test.avi')

while(1):
    
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    img_rect1 = gray[345:345+40, 335:335+70]#(y,x)
    img_out1[345:345+40, 335:335+70] = img_rect1.copy()
    ret,thresh1 = cv2.threshold(img_out1,100,255,cv2.THRESH_BINARY)
    kernel = np.ones((3,3),np.uint8)
    dilate1 = cv2.dilate(thresh1,kernel,iterations = 2)
    
    area = []
    max_idx = None
    contours, hierarchy = cv2.findContours(dilate1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):

        area.append(cv2.contourArea(contours[c]))
        max_idx = np.argmax(area)

        if(max_idx!=None):
            rect = cv2.minAreaRect(contours[max_idx])
            cx, cy = rect[0]
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            length1=math.pow((box[1][1]-box[0][1]),2)+math.pow((box[1][0]-box[0][0]),2)
            length2=math.pow((box[2][1]-box[1][1]),2)+math.pow((box[2][0]-box[1][0]),2)
            if length1<length2:
                pointx_centerline,pointy_centerline = (box[2][0]-box[1][0])/2+box[1][0],(box[2][1]-box[1][1])/2+box[1][1]
            else:
                pointx_centerline,pointy_centerline = (box[1][0]-box[0][0])/2+box[0][0],(box[1][1]-box[0][1])/2+box[0][1]            
            
            cv2.drawContours(frame,[box],0,(0,255,0),2)
            cv2.circle(frame, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, 8, 0)
            cv2.circle(frame, (np.int32(pointx_centerline), np.int32(pointy_centerline)), 2, (0, 0, 255), 2, 8, 0)
            
    #cv2.imshow('frame1',dilate1)##wan
    
    
    
    img_rect2 = gray[410:410+100, 410:410+145]
    ret,img_rect2 = cv2.threshold(img_rect2,80,255,cv2.THRESH_BINARY_INV)
    img_out2[410:410+100, 410:410+145] = img_rect2.copy()
    ret,thresh2 = cv2.threshold(img_out2,80,255,cv2.THRESH_BINARY)
    erode2 = cv2.erode(thresh2,kernel,iterations = 1)
    dilate2 = cv2.dilate(erode2,kernel,iterations = 2)

    area = []
    max_idx = None
    contours, hierarchy = cv2.findContours(dilate2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):

        area.append(cv2.contourArea(contours[c]))
        max_idx = np.argmax(area)

        if(max_idx!=None):
            rect = cv2.minAreaRect(contours[max_idx])
            cx, cy = rect[0]
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            length1=math.pow((box[1][1]-box[0][1]),2)+math.pow((box[1][0]-box[0][0]),2)
            length2=math.pow((box[2][1]-box[1][1]),2)+math.pow((box[2][0]-box[1][0]),2)
            if length1<length2:
                pointx_centerline,pointy_centerline = (box[2][0]-box[1][0])/2+box[1][0],(box[2][1]-box[1][1])/2+box[1][1]
            else:
                pointx_centerline,pointy_centerline = (box[1][0]-box[0][0])/2+box[0][0],(box[1][1]-box[0][1])/2+box[0][1]
            
            cv2.circle(frame, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, 8, 0)
            cv2.drawContours(frame,[box],0,(0,255,0),2)
            cv2.circle(frame, (np.int32(pointx_centerline), np.int32(pointy_centerline)), 2, (0, 0, 255), 2, 8, 0)
            cv2.line(frame, (np.int32(cx),np.int32(cy)), (np.int32(pointx_centerline), np.int32(pointy_centerline)), (0, 255, 0), 1)
    #cv2.imshow('frame2',dilate2)
    
    
    
    img_rect3 = gray[326:326+30, 526:526+60]
    img_out3[326:326+30, 526:526+60] = img_rect3.copy()
    ret,thresh3 = cv2.threshold(img_out3,100,255,cv2.THRESH_BINARY)
    dilate3 = cv2.dilate(thresh3,kernel,iterations = 2)

    area = []
    max_idx = None
    contours, hierarchy = cv2.findContours(dilate3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):

        area.append(cv2.contourArea(contours[c]))
        max_idx = np.argmax(area)

        if(max_idx!=None):
            rect = cv2.minAreaRect(contours[max_idx])
            cx, cy = rect[0]
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            length1=math.pow((box[1][1]-box[0][1]),2)+math.pow((box[1][0]-box[0][0]),2)
            length2=math.pow((box[2][1]-box[1][1]),2)+math.pow((box[2][0]-box[1][0]),2)
            if length1<length2:
                pointx_centerline,pointy_centerline = (box[2][0]-box[1][0])/2+box[1][0],(box[2][1]-box[1][1])/2+box[1][1]
            else:
                pointx_centerline,pointy_centerline = (box[1][0]-box[0][0])/2+box[0][0],(box[1][1]-box[0][1])/2+box[0][1]
                
            cv2.drawContours(frame,[box],0,(0,255,0),2)
            cv2.circle(frame, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, 8, 0)
            cv2.circle(frame, (np.int32(pointx_centerline), np.int32(pointy_centerline)), 2, (0, 0, 255), 2, 8, 0)
            cv2.line(frame, (np.int32(cx),np.int32(cy)), (np.int32(pointx_centerline), np.int32(pointy_centerline)), (0, 255, 0), 1)
    #cv2.imshow('frame3',dilate3)
    
    
    
    
    cv2.imshow('frame',frame)
    
    cv2.waitKey(1)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    
cap.release()

cv2.destroyAllWindows()
