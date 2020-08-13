#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import math

img_out1 = np.zeros((540,960),dtype=np.uint8)
img_out2 = np.zeros((540,960),dtype=np.uint8)
img_out3 = np.zeros((540,960),dtype=np.uint8)

bar_pose = np.zeros(9,dtype=float)

def model_detection(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
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
            if length1>length2:
                pointx_centerline,pointy_centerline = (box[2][0]-box[1][0])/2+box[1][0],(box[2][1]-box[1][1])/2+box[1][1]
                theta_pan = math.atan2((box[3][1]-box[0][1]),(box[3][0]-box[0][0]))+math.pi
            else:
                pointx_centerline,pointy_centerline = (box[1][0]-box[0][0])/2+box[0][0],(box[1][1]-box[0][1])/2+box[0][1]
                theta_pan = math.atan2((box[1][1]-box[0][1]),(box[1][0]-box[0][0]))+math.pi       
            
            cv2.drawContours(img,[box],0,(0,255,0),2)
            cv2.circle(img, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, 8, 0)
            cv2.circle(img, (np.int32(pointx_centerline), np.int32(pointy_centerline)), 2, (0, 0, 255), 2, 8, 0)
            
            #print("pan",cx,cy,depth_img[int(cy),int(cx)])
            #x1,y1,z1=calibra_instance.Pix2baselink_points(depth_img[int(cy),int(cx)],cx,cy)
            
            #print("base_pan",x1,y1,z1,theta_pan*180/math.pi)
            #rx1,ry1,rz1=calibra_instance.rpy2rotvec(-math.pi/2,0,(theta_pan+math.pi/2))
            bar_pose[0],bar_pose[1],bar_pose[2] = cx, cy, theta_pan
            #print("base_pan_rotation",cx,cy,theta_pan)


    
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
            if length1>length2:
                pointx_centerline,pointy_centerline = (box[2][0]-box[1][0])/2+box[1][0],(box[2][1]-box[1][1])/2+box[1][1]
                theta_cai = math.atan2((box[3][1]-box[0][1]),(box[3][0]-box[0][0]))
            else:
                pointx_centerline,pointy_centerline = (box[1][0]-box[0][0])/2+box[0][0],(box[1][1]-box[0][1])/2+box[0][1]
                theta_cai = math.atan2((box[1][1]-box[0][1]),(box[1][0]-box[0][0]))+math.pi
            #print("~~~~~~~~~~~~~~~~~",box)
            cv2.circle(img, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, 8, 0)
            cv2.drawContours(img,[box],0,(0,255,0),2)
            #cv2.circle(img, (np.int32(pointx_centerline), np.int32(pointy_centerline)), 2, (0, 0, 255), 2, 8, 0)
            
            cv2.circle(img, (np.int32(box[0][0]), np.int32(box[0][1])), 2, (0, 0, 255), 2, 8, 0)
            cv2.circle(img, (np.int32(box[1][0]), np.int32(box[1][1])), 2, (0, 255, 0), 2, 8, 0)
            cv2.line(img, (np.int32(cx),np.int32(cy)), (np.int32(pointx_centerline), np.int32(pointy_centerline)), (0, 255, 0), 1)
            #cv2.imshow('frame2',dilate2)
            #print("cai",cx,cy,depth_img[int(cy),int(cx)])
            #x2,y2,z2=calibra_instance.Pix2baselink_points(depth_img[int(cy),int(cx)],cx,cy)
            #print("zzzzzzzzzzzzzzzzzzzz",depth_img[int(cy),int(cx)])
            #print("base_cai",x2,y2,z2,theta_cai*180/math.pi)
            #rx,ry,rz=calibra_instance.rpy2rotvec(-math.pi/2,0,(theta_cai+math.pi/2))
            theta_cai = theta_cai
            bar_pose[3],bar_pose[4],bar_pose[5] = cx, cy, theta_cai
            #print("base_cai_pos_uv",cx,cy,theta_cai)

            
    img_rect3 = gray[326:326+30, 526:526+60+40]
    img_out3[326:326+30, 526:526+60+40] = img_rect3.copy()
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
            if length1>length2:
                pointx_centerline,pointy_centerline = (box[2][0]-box[1][0])/2+box[1][0],(box[2][1]-box[1][1])/2+box[1][1]
                theta_pot = math.atan2((box[3][1]-box[0][1]),(box[3][0]-box[0][0]))+math.pi
            else:
                pointx_centerline,pointy_centerline = (box[1][0]-box[0][0])/2+box[0][0],(box[1][1]-box[0][1])/2+box[0][1]
                theta_pot = math.atan2((box[1][1]-box[0][1]),(box[1][0]-box[0][0]))+math.pi
            cv2.drawContours(img,[box],0,(0,255,0),2)
            cv2.circle(img, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, 8, 0)
            cv2.circle(img, (np.int32(pointx_centerline), np.int32(pointy_centerline)), 2, (0, 0, 255), 2, 8, 0)
            cv2.line(img, (np.int32(cx),np.int32(cy)), (np.int32(pointx_centerline), np.int32(pointy_centerline)), (0, 255, 0), 1)
            #cv2.imshow('frame3',dilate3)
            
            #print("souppot",cx,cy,depth_img[int(cy),int(cx)])
            #x3,y3,z3=calibra_instance.Pix2baselink_points(depth_img[int(cy),int(cx)],cx,cy)
            #print("base_souppot",x3,y3,z3,theta_pot*180/math.pi)


            #rx3,ry3,rz3=calibra_instance.rpy2rotvec(-math.pi/2,0,(theta_pot+math.pi/2))
            bar_pose[6],bar_pose[7],bar_pose[8] = cx, cy, theta_pot
            #print("souppot_pos",cx,cy,theta_pot)
    #cv2.imshow('frame',img)  
    cv2.waitKey(1)
    return bar_pose

