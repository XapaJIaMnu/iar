# -*- coding: utf-8 -*-
# export PYTHONPATH=$PYTHONPATH:~/Downloads/python/
import serial
import time
import Reactive
import plot
from math import sqrt

serial = serial.Serial('/dev/ttyS0')

class Robot:
    def __init__(self):
        self.starttime = time.time()
        global serial
        self.serial = serial
        self.reactive = Reactive.Reactive(self.serial);

    def start(self):
        while(True):
            self.reactive.act(0)
            time.sleep(0.05)
            print "Distance from home " + str(self.reactive.sensors.getDistanceFromHome())
            print "Angle from home " + str(self.reactive.sensors.getAngleFromHome())
            if (time.time() - self.starttime) > 30:
              self.serial.write('D,0,0\n')
              self.serial.readline()
              break
 
    def stop(self):
        self.serial.write('D,0,0\n')
        self.serial.readall()

def stop():
    serial.write('D,0,0\n')
    serial.readall()

robot = Robot()
