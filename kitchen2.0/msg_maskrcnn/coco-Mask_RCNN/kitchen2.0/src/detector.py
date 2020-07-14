#!/usr/bin/env python
from kitchen.msg import objs
from kitchen.msg import obj

class Detector:
    def __init__(self):
        self.detectSucess = False

    def detect(self, vis):
        self.detectSucess = True
        detectedObjs = objs()
        
        a = obj()
        a.id = 1
        a.classname = "beef"
        a.probability = 0.99
        a.roi.x_offset = 5
        a.roi.y_offset = 6
        a.roi.width = 7
        a.roi.height = 8
        a.pose.position.x = 9
        a.pose.position.y = 10
        a.pose.position.z = 11
        a.pose.orientation.x = 0.1
        a.pose.orientation.y = 0.2
        a.pose.orientation.z = 0.3
        a.pose.orientation.w = 0.4
        b = obj() 
        b.id = 2
        b.classname = "broccoli"
        b.probability = 0.99
        b.roi.x_offset = 5
        b.roi.y_offset = 6
        b.roi.width = 7
        b.roi.height = 8
        b.pose.position.x = 9
        b.pose.position.y = 10
        b.pose.position.z = 11
        b.pose.orientation.x = 0.1
        b.pose.orientation.y = 0.2
        b.pose.orientation.z = 0.3
        b.pose.orientation.w = 0.4
        detectedObjs.objects_vector.append(a)
        detectedObjs.objects_vector.append(b)
        print("detector")

        return detectedObjs
