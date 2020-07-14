# Copyright (c) 2017 Roomin Corporation

int32[] id   #lll
string[] classname  # object class name
float32[] score # probability of detected object
sensor_msgs/RegionOfInterest[] roi  # region of interest
# Instance masks as Image
sensor_msgs/Image[] masks
