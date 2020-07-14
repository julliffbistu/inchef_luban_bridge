#!/usr/bin/env python
from kitchen.msg import objs
from kitchen.msg import events

import rospy
from geometry_msgs.msg import Pose, PoseStamped
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import String

class LBFunc:
    def __init__(self, api_name, topic, data_class):
        self.api_name = api_name
        self.topic = topic
        self.data_class = (data_class)
        if data_class is None:
            raise ValueError("topic parameter 'data_class' is not initialized")
        if not type(data_class) == type:
            raise ValueError("data_class [%s] is not a class"%data_class)

api_list = { #17 api
    LBFunc("checkenv","luban_bridge/checkenv", Bool), #check env,
    LBFunc("getbeefcenterpose","luban_bridge/getbeefcenterpose", Pose), # get beef center pose
    LBFunc("checkbeefdrop","luban_bridge/checkbeefdrop", Bool)# check beef dropped
}

class Bridge:

    def __init__(self):
        self.objects_sub = rospy.Subscriber("processor/objs",objs,self.callbackobjs)
        self.events_sub = rospy.Subscriber("processor/events",events,self.callbackevents)
        self.pub_handle = {}
        print("init func list:")
        i = 0
        for al in (api_list):
            print(al)
            self.pub_handle[i] = rospy.Publisher(al.topic,al.data_class,queue_size=10)
            i =i+1

    def find_handler(self, name):
        i = 0
        for al in (api_list):
            if(al.api_name == name):
                return self.pub_handle[i] 
            i =i+1
        return NotImplementedError

    def callbackobjs(self,objs):
        print("some callback")
        
    def callbackevents(self,events):
        print("test callback")
    

if __name__ == '__main__':
    bridge = Bridge()
    rospy.init_node('luban_bridger',anonymous = True)
    try:
        #test
        bridge.find_handler("checkenv").publish(True)
        
        #while
        rospy.spin()
        print("luban_bridge node exit!")
    except KeyboardInterrupt:
        print("Shutting Down") 

