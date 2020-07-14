# -*- coding:UTF-8 -*-
#!/usr/bin/env python
import rospy
import roslib
#from后边是自己的包.msg，也就是自己包的msg文件夹下，test是我的msg文件名test.msg
from kitchen.msg import obj
from kitchen.msg import objs

import cv2
import numpy as np
from PIL import Image
from cv_bridge import CvBridge

def callback(data):
    '''
    print(data.objects_vector[0].id)
    print(data.objects_vector[0].classname)
    print(data.objects_vector[0].score)
    print(data.objects_vector[0].roi)
    print("**********")

    print(data.objects_vector[0].id[0])
    print(data.objects_vector[0].classname[0])
    print(data.objects_vector[0].score[0])
    print(data.objects_vector[0].roi[0])
    print(data.objects_vector[0].roi[0].x_offset)
    print(data.objects_vector[0].roi[0].y_offset)
    print(data.objects_vector[0].roi[0].height)
    print(data.objects_vector[0].roi[0].width)
    print(data.objects_vector[0].masks[0])

    print(data.header)
    print("----changdu-----",len(data.objects_vector[0].id))
    print("----"*15)
    '''

    get_msg = data.objects_vector[0]

    for i in range(len(get_msg.id)):
        if get_msg.score[i] >= 0.8:
            
            if get_msg.classname[i] == "beef":
                print("count----:",i)
    print("**********")
    print(data.objects_vector[0].masks[0].height)
    print(data.objects_vector[0].masks[0].width)
    print(data.header)
    #cimgmask =np.uint8(get_msg.masks[0])
    #temp_mask=cimgmask*255
    bridge=CvBridge()
    cv_image =bridge.imgmsg_to_cv2(data.rgb_img,"bgr8")
    cv2.imshow("img",cv_image)

    cv_depth_image = bridge.imgmsg_to_cv2(data.depth_img,"passthrough")
    print(cv_depth_image)
    cv2.waitKey(1)
    '''
    print(get_msg.id)
    print(get_msg.classname)
    print(get_msg.score)
    print(get_msg.roi)
    print("**********")

    print(get_msg.id[0])
    print(get_msg.classname[0])
    print(get_msg.score[0])
    print(get_msg.roi[0])
    print(get_msg.roi[0].x_offset)
    print(get_msg.roi[0].y_offset)
    print(get_msg.roi[0].height)
    print(get_msg.roi[0].width)
    print(get_msg.masks[0])

    print(data.header)
    print("----changdu-----",len(get_msg.id))
    print("----"*15)
    '''


def listener():
 
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("processor/objs", objs, callback)

    rospy.spin()
 
if __name__ == '__main__':
    listener()
