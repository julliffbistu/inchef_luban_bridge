# -*- coding:UTF-8 -*-
#!/usr/bin/env python
import rospy
import roslib
#from后边是自己的包.msg，也就是自己包的msg文件夹下，test是我的msg文件名test.msg
from inchef_dl_msgs.msg import obj
from inchef_dl_msgs.msg import objs

import cv2
import numpy as np
from PIL import Image
from cv_bridge import CvBridge

from inchef_dl_msgs.msg import sglobj
from inchef_dl_msgs.msg import listobj

def prcess_contours(cv_image, classname, masks_img, mask_id, x, y, width, height, scores):
    list_info=[]
    #print("max : ",i,classname)
    contours, hierarchy = cv2.findContours(masks_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):
        #Area = cv2.contourArea(contours[c])

        rect = cv2.minAreaRect(contours[c])
        box = cv2.boxPoints(rect)#得到端点
        box = np.int0(box)#向下取整
        cv2.drawContours(cv_image,[box],0,(0,255,0),1)

        cv2.rectangle(cv_image,(x, y),(x+height, y+width),(255,0,0),2)
        #print("***********",[x, y,x+height, y+width])
        #cx1, cy1 = rect[0] #min area center
        cx1 = int (x + height/2) # rect area center
        cy1 = int (y + width/2) # rect area center

        cv2.circle(cv_image, (np.int32(cx1), np.int32(cy1)), 6, (0,0,255), -1)
        cv2.drawContours(cv_image, contours, c, (0, 0, 255), 1, 8)

        score=scores if scores is not None else None
        caption='{}{:.2f}'.format(classname,scores) if scores else classname
        image=cv2.putText(cv_image,caption,(x, y),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),2)


        grasp_delta = 20 #pixcel
        grasp_left_x = int(cx1 - height/2 - grasp_delta)
        grasp_left_y = cy1 
        grasp_right_x = int(cx1 + height/2 + grasp_delta)
        grasp_right_y = cy1
        cv2.circle(cv_image, (np.int32(grasp_left_x), np.int32(grasp_left_y)), 6, (0,0,255), -1)
        cv2.circle(cv_image, (np.int32(grasp_right_x), np.int32(grasp_right_y)), 6, (0,0,255), -1)
        im = cv2.line(cv_image, (np.int32(grasp_left_x),np.int32(grasp_left_y)), 
            (np.int32(grasp_right_x), np.int32(grasp_right_y)), (0, 255, 255), 1)

        number = int(len(contours[c])/4)
        press1_x,press1_y = int(contours[c][0][0][0]), int(contours[c][0][0][1])
        press2_x,press2_y = int(contours[c][number*1][0][0]), int(contours[c][number*1][0][1])
        press3_x,press3_y = int(contours[c][number*2][0][0]), int(contours[c][number*2][0][1])
        press4_x,press4_y = int(contours[c][number*3][0][0]), int(contours[c][number*3][0][1])
        cv2.circle(cv_image, (press1_x,press1_y), 3, (0,0,0), -1)
        cv2.circle(cv_image, (press2_x,press2_y), 3, (0,0,0), -1)
        cv2.circle(cv_image, (press3_x,press3_y), 3, (0,0,0), -1)
        cv2.circle(cv_image, (press4_x,press4_y), 3, (0,0,0), -1)

        grasp_left_theta = int(180)
        grasp_right_theta = int(0)
        mask_id = int(mask_id)

        list_info = [int(mask_id), int(grasp_left_x),int(grasp_left_y),int(grasp_left_theta),
        int(grasp_right_x),int(grasp_right_y),int(grasp_right_theta),int(cx1),int(cy1),
        int(press1_x),int(press1_y),int(press2_x),int(press2_y),int(press3_x),int(press3_y),int(press4_x),int(press4_y)]
        #print("111111111:",list_info)

        return list_info


def callback(data):

    print(data.objects_vector[0].id)
    print(data.objects_vector[0].classname)
    print(data.objects_vector[0].score)
    print("---"*20)

    single_obj = sglobj()
    single_obj.id_info = []
    single_obj.classname = []
    single_obj.score = []

    get_msg = data.objects_vector[0]
    bridge=CvBridge()
    cv_image =bridge.imgmsg_to_cv2(data.rgb_img,"bgr8")
    cv_depth_image = bridge.imgmsg_to_cv2(data.depth_img,"passthrough")
    rgb_img_to_pos = cv_image.copy()
    depth_img_to_pos = cv_depth_image.copy()

    plate_score=[0,0]
    pan_score=[0]
    vegetablebowl_score=[0]
    broccoli_score=[0,0,0]
    souppothandle_score=[0]
    panhandle_score=[0]
    beef_score=[0]
    nethandle_score=[0]
    seasoningbottle_score=[0,0]
    seasoningbowl_score=[0]

    for i in range(len(get_msg.id)):
        if(get_msg.classname[i] == "pan"):
            pan_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "beef"):
            beef_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "plate"):
            plate_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "vegetablebowl"):
            vegetablebowl_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "broccoli"):
            broccoli_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "souppothandle"):
            souppothandle_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "panhandle"):
            panhandle_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "seasoningbowl"):
            beef_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "nethandle"):
            nethandle_score.append(get_msg.score[i])
        if(get_msg.classname[i] == "seasoningbottle"):
            seasoningbottle_score.append(get_msg.score[i])

    plate_score = sorted(plate_score,reverse=True)
    pan_score = sorted(pan_score,reverse=True)
    vegetablebowl_score = sorted(vegetablebowl_score,reverse=True)
    broccoli_score = sorted(broccoli_score,reverse=True)
    souppothandle_score = sorted(souppothandle_score,reverse=True)
    panhandle_score = sorted(panhandle_score,reverse=True)
    beef_score = sorted(beef_score,reverse=True)
    nethandle_score = sorted(nethandle_score,reverse=True)
    seasoningbottle_score = sorted(seasoningbottle_score,reverse=True)
    seasoningbowl_score = sorted(seasoningbowl_score,reverse=True)

    '''
    print("plate score :           ",plate_score)
    print("pan score :             ",pan_score)
    print("vegetablebowl score :   ",vegetablebowl_score)
    print("broccoli score :        ",broccoli_score)
    print("souppothandle score :   ",souppothandle_score)
    print("panhandle score :       ",panhandle_score)
    print("beef score :            ",beef_score)
    print("nethandle score :       ",nethandle_score)
    print("seasoningbottle score : ",seasoningbottle_score)
    print("seasoningbowl score :  ",seasoningbowl_score)
    '''

    list_obj = listobj()
    list_obj.single_obj_info = []

    single_obj.id_info = []
    single_obj.classname = []
    single_obj.score = []
    for i in range(len(get_msg.id)):

        mask_area = get_msg.roi[i].height * get_msg.roi[i].width
        if mask_area > 0 and get_msg.score[i] > 0.0:

            mask_image =bridge.imgmsg_to_cv2(get_msg.masks[i],"passthrough")

            if get_msg.classname[i] == "plate" and get_msg.score[i] == plate_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])
            
            if get_msg.classname[i] == "plate" and get_msg.score[i] == plate_score[1]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])
                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])
            
            if get_msg.classname[i] == "beef" and get_msg.score[i] == beef_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i], 
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "pan" and get_msg.score[i] == pan_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "broccoli" and get_msg.score[i] == broccoli_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                for number in range(len(temp_list)):
                    single_obj.id_info.append(temp_list[number])
                single_obj.classname.append(get_msg.classname[i])
                single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "broccoli" and get_msg.score[i] == broccoli_score[1]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "broccoli" and get_msg.score[i] == broccoli_score[2]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "souppothandle" and get_msg.score[i] == souppothandle_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "nethandle" and get_msg.score[i] == nethandle_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "vegetablebowl" and get_msg.score[i] == vegetablebowl_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "seasoningbowl" and get_msg.score[i] == seasoningbowl_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "seasoningbottle" and get_msg.score[i] == seasoningbottle_score[0]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "seasoningbottle" and get_msg.score[i] == seasoningbottle_score[1]:
                temp_list = []
                temp_list = prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

            if get_msg.classname[i] == "panhandle" and get_msg.score[i] == panhandle_score[0]:
                temp_list = []
                prcess_contours(cv_image, get_msg.classname[i], mask_image, get_msg.id[i],
                get_msg.roi[i].x_offset, get_msg.roi[i].y_offset, get_msg.roi[i].height, get_msg.roi[i].width, get_msg.score[i])

                if len(temp_list)>0:
                    for number in range(len(temp_list)):
                        single_obj.id_info.append(temp_list[number])
                    single_obj.classname.append(get_msg.classname[i])
                    single_obj.score.append(get_msg.score[i])

    if len(single_obj.id_info)>0:
        #print("1111:",single_obj)
        #print("222222")
        list_obj.single_obj_info.append(single_obj)

    #print("1111:",list_obj.single_obj_info)
    list_obj.header.stamp = data.header.stamp
    list_obj.header.frame_id = data.header.frame_id
    print("------------------------")
    list_obj.rgb_img_to_pos = bridge.cv2_to_imgmsg(rgb_img_to_pos, encoding="bgr8")
    list_obj.depth_img_to_pos = bridge.cv2_to_imgmsg(depth_img_to_pos,"passthrough")

    #print("1111:",list_obj)
    list_obj_pub = rospy.Publisher("process_uv/listobjs",listobj,queue_size=1)
    list_obj_pub.publish(list_obj)

    cv2.imshow("img2",cv_image)
    cv2.waitKey(1)


def listener():
 
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("processor/objs", objs, callback)

    rospy.spin()
 
if __name__ == '__main__':
    listener()
