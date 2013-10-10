# -*- coding: utf-8 -*-
# export PYTHONPATH=$PYTHONPATH:~/Downloads/python/
import serial
import time
import Reactive
from math import sqrt

class Robot:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyS0')
        self.reactive = Reactive.Reactive(self.serial);

    def start(self):
        while(True):
            self.reactive.act(0)
            time.sleep(0.05)
 
    def stop(self):
        self.serial.write('D,0,0\n')
        self.serial.readall()

robot = Robot()
