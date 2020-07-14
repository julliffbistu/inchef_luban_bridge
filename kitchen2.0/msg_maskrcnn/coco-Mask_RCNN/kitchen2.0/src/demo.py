#! /usr/bin/env python
import roslib
import sys
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from detector import Detector
from tracker import Tracker
from sanitychecker import Checker
from kitchen.msg import objs
from kitchen.msg import events

class mainprocessor:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/kinect2/hd/image_color1",Image,self.callback)
        self.objects_pub = rospy.Publisher("processor/objs",objs,queue_size=10)
        self.events_pub = rospy.Publisher("processor/events",events,queue_size=10)
        self.checker = Checker()
        self.detector = Detector()
        self.tracker = Tracker()
        

    def callback(self, image):
        cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
        #cv2.imshow("img",cv_image)
        sanityevents = self.checker.check(cv_image)

        detectedObjs = self.detector.detect(cv_image)
        trackedObjs = self.tracker.track(cv_image,detectedObjs) 
        print(detectedObjs)
        print(sanityevents)
        self.objects_pub.publish(detectedObjs)
        self.events_pub.publish(sanityevents)
        
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    rospy.signal_shutdown('Quit')
        #    cv2.destroyAllWindows()       

if __name__ == '__main__':
    processor = mainprocessor()
    rospy.init_node('processor',anonymous = True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down") 
    cv2.destroyAllWindows()
