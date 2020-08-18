import cv2
import numpy as np
from matplotlib import patches,  lines

out = cv2.VideoWriter('broccoli_detect.avi',cv2.VideoWriter_fourcc('M','J','P','G'),30,(960,540))
 
# set blue thresh 设置HSV中蓝色、天蓝色范围
lower_blue = np.array([36,43,46])
upper_blue = np.array([77,255,255])

img_out = np.zeros((540,960,3),dtype=np.uint8)

cap = cv2.VideoCapture('a.avi')

while(1):
    # get a frame and show 获取视频帧并转成HSV格式, 利用cvtColor()将BGR格式转成HSV格式，参数为cv2.COLOR_BGR2HSV。
    
    ret, frame = cap.read()
    
    rect1 = frame[340:490, 90:270]#(90,340) (270,490)
    rect2 = frame[190:330, 645:810]#(645,200) (810,330)
    
    cv2.rectangle(frame,(90,340),(270,490),(0,255,0),2)
    
    img_out[340:490, 90:270] = rect1.copy()
    img_out[190:330, 645:810] = rect2.copy()
    
    #cv2.imshow('img_out', img_out)
    
    # change to hsv model
    hsv = cv2.cvtColor(img_out, cv2.COLOR_BGR2HSV)

    # get mask 利用inRange()函数和HSV模型中蓝色范围的上下界获取mask，mask中原视频中的蓝色部分会被弄成白色，其他部分黑色。
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    
    ret,thresh = cv2.threshold(mask,100,255,cv2.THRESH_BINARY)
    
    kernel = np.ones((3,3),np.uint8)
    erode_img = cv2.erode(thresh,kernel,iterations = 1)
    dilate_img = cv2.dilate(erode_img,kernel,iterations = 1)
    
    #cv2.imshow('Mask', dilate_img)
    contours, hierarchy = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    number = 0
    for c in range(len(contours)):
        Area = cv2.contourArea(contours[c])
        if Area > 170:
            number = number + 1
            rect = cv2.minAreaRect(contours[c])
            cx, cy = rect[0]
            x,y,w,h = cv2.boundingRect(contours[c])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
            cv2.circle(frame, (np.int32(cx), np.int32(cy)), 6, (0,0,255), -1)
            cv2.drawContours(frame, contours, c, (0, 0, 255), 2, 8)
        
        
        
        
    print("西兰花个数：",number)
    # detect green 将mask于原视频帧进行按位与操作，则会把mask中的白色用真实的图像替换：
    #res = cv2.bitwise_and(frame, frame, mask=mask)
    #cv2.imshow('Result', res)
    cv2.waitKey(30)
    
    out.write(frame)
    cv2.imshow('Capture', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()