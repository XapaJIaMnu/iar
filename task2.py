# -*- coding: utf-8 -*-
# export PYTHONPATH=$PYTHONPATH:~/Downloads/python/
import serial
import time
import Reactive
import plot
from math import sqrt

serial = serial.Serial('/dev/ttyS0')

IPLOT=True

TURNING_TOWARDS_HOME = False 
ANGLE_THRESH = 3 
ANGLE_PRECISE_THRESH = 20
ANGLE_CAREFUL_THRESH = 10
DIST_THRESH = 5
DEFAULT_SPEED_ACTIVE = 0.05
DEFAULT_SPEED_HOME = 0.05
EXPLORE_FOR = 10

class Robot:
    def __init__(self):
        global serial
        self.serial = serial
        self.reactive = Reactive.Reactive(self.serial);
        if IPLOT:
            self.ip = plot.InteractivePlot()

    def start(self):
        global TURNING_TOWARDS_HOME
        global ANGLE_THRESH
        global DIST_THRESH 
        global ANGLE_PRECISE_THRESH
        global DEFAULT_SPEED_ACTIVE
        global DEFAULT_SPEED_HOME
        global EXPLORE_FOR
        self.starttime = time.time()
        suggestAction = 0
        perceive_speed = DEFAULT_SPEED_ACTIVE
        while(True):
            print
            print
            extra_sleep = 0
            self.reactive.sensors.updateModel()
            if IPLOT:
                self.ip.update(robot.reactive.sensors.historyPosX, robot.reactive.sensors.historyPosY)
            if TURNING_TOWARDS_HOME:
                self.serial.write('D,0,0\n')
                self.serial.readline()
                time.sleep(0.1)
                self.reactive.sensors.updateModel()
                self.reactive.sensors.updatePos()
                angle = (180-robot.reactive.sensors.getAngleToHome())%360
                other_angle = 360-angle
                print "Turning towards home angle is " + str(angle)
                if  angle > ANGLE_THRESH and other_angle > ANGLE_THRESH:
                    if angle < ANGLE_PRECISE_THRESH or other_angle < ANGLE_PRECISE_THRESH:
                        turnSpeed = 1
                    elif angle < ANGLE_CAREFUL_THRESH or other_angle < ANGLE_CAREFUL_THRESH:
                        turnSpeed = 2
                    else:
                        turnSpeed = -1
                    if angle > 180:
                        print "Suggesting left"
                        suggestAction = ("turnRight", turnSpeed)
                    else:
                        print "Suggesting right"
                        suggestAction = ("turnLeft", turnSpeed)
                else:
                    print "Going home!"
                    distToHome = self.reactive.sensors.getDistanceFromHome()
                    if distToHome > DIST_THRESH:
                        suggestAction = ("goStraight", 5)
                        extra_sleep += 0.1
                    else:
                        print "Home!!!"
                        return
            self.reactive.act(suggestAction)
            time.sleep(perceive_speed + extra_sleep)
            print "Distance from home " + str(self.reactive.sensors.getDistanceFromHome())
            print "Angle from home " + str(self.reactive.sensors.getAngleFromHome())
            if (time.time() - self.starttime) > EXPLORE_FOR:
              self.serial.write('D,0,0\n')
              self.serial.readline()
   #           plot.plotPath(robot.reactive.sensors.historyPosX, robot.reactive.sensors.historyPosY)
              TURNING_TOWARDS_HOME = True
              perceive_speed = DEFAULT_SPEED_HOME
              #self.distToHome = self.reactive.sensors.getDistanceFromHome()
 
    def stop(self):
        self.serial.write('D,0,0\n')
        self.serial.readall()

def stop():
    serial.write('D,0,0\n')
    serial.readall()

robot = Robot()
