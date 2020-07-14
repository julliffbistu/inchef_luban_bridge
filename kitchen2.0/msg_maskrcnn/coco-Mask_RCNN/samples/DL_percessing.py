# -*- coding:UTF-8 -*-
#!/usr/bin/env python
import rospy
import roslib
#from后边是自己的包.msg，也就是自己包的msg文件夹下，test是我的msg文件名test.msg
from kitchen.msg import obj
from kitchen.msg import objs


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



def listener():
 
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("processor/objs", objs, callback)

    rospy.spin()
 
if __name__ == '__main__':
    listener()
