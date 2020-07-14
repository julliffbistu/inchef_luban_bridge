#!/usr/bin/env python
from kitchen.msg import events

class Checker:
    def __init__(self):
        self.checkSucess = False

    def check(self, vis):
        sanityevents = events()
        sanityevents.events.append("BeefReady")
        sanityevents.events.append("CameraReady")
        
        self.checkSucess = True
        return sanityevents
        
