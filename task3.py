# -*- coding: utf-8 -*-
# export PYTHONPATH=$PYTHONPATH:~/Downloads/python/
import serial
import time
import Reactive
import plot
from math import sqrt
# import pygame

serial = serial.Serial('/dev/ttyS0')

IPLOT=True

TURNING_TOWARDS_HOME = False
GOING_TOWARDS_FOOD = False 
ANGLE_THRESH = 3 
ANGLE_PRECISE_THRESH = 20
ANGLE_CAREFUL_THRESH = 10
DIST_THRESH = 8
DIST_NEAR = 60
DEFAULT_SPEED_ACTIVE = 0.05
DEFAULT_SPEED_HOME = 0.05
EXPLORE_FOR = 30

name = "IAR"

class Robot:
    def __init__(self):
        global serial
        global name

        #pygame.init()        

        #self.windowSurfaceObj = pygame.display.set_mode((640, 480))
        #pygame.display.set_caption(name)

        #self.mapSurfaceObj = pygame.image.load('arena.jpg')        

        self.serial = serial
        self.reactive = Reactive.Reactive(self.serial);
        if IPLOT:
            self.ip = plot.InteractivePlot()

    def start(self):
        global TURNING_TOWARDS_HOME
        global ANGLE_THRESH
        global DIST_THRESH
        global DIST_NEAR
        global ANGLE_PRECISE_THRESH
        global DEFAULT_SPEED_ACTIVE
        global DEFAULT_SPEED_HOME
        global EXPLORE_FOR
        global GOING_TOWARDS_FOOD
        self.starttime = time.time()
        prevDistToHome = 100000
        prevDistToFood = 100000
        suggestAction = 0
        perceive_speed = DEFAULT_SPEED_ACTIVE
        while(True):
            #self.windowSurfaceObj.blit(self.mapSurfaceObj, (0, 0))
            print
            print
            extra_sleep = 0
            self.reactive.sensors.updateModel()
            if IPLOT:
                self.ip.update(robot.reactive.sensors.historyPosX, robot.reactive.sensors.historyPosY)

            prevx, prevy = (0, 0)
            #for (x, y) in zip(robot.reactive.sensors.historyPosX, robot.reactive.sensors.historyPosY):
            #    pygame.draw.line(windowSurfaceObj, (0, 0, 255), (prevx, prevy), (x, y))
            #    prevx, prevy = (x, y)

            if GOING_TOWARDS_FOOD:
                #self.serial.write('D,0,0\n')
                #self.serial.readline()
                #time.sleep(0.1)
                self.reactive.sensors.updateModel()
                self.reactive.sensors.updatePos()
                angle = (180-robot.reactive.sensors.getAngleToFood())%360
                other_angle = 360-angle
                print "Turning towards food angle is " + str(angle) + " other one is " + str(other_angle)


                distToFood = self.reactive.sensors.getDistanceFromFood()

                if distToFood < DIST_NEAR and distToFood > prevDistToFood:
                    print "Food!!!"
                    self.serial.write('D,0,0\n')
                    self.serial.readline()
                    if self.reactive.sensors.haveFood == True:
                        print "Food!!!"
                        self.reactive.sensors.haveFood = False
                        self.serial.write('D,0,0\n')
                        self.serial.readline()
                        TURNING_TOWARDS_HOME = True
                        GOING_TOWARDS_FOOD = False

                if  angle > ANGLE_THRESH and other_angle > ANGLE_THRESH:
                    if angle < ANGLE_PRECISE_THRESH or other_angle < ANGLE_PRECISE_THRESH:
                        turnSpeed = 1
                    elif angle < ANGLE_CAREFUL_THRESH or other_angle < ANGLE_CAREFUL_THRESH:
                        turnSpeed = 2
                    else:
                        turnSpeed = -1
                    if angle > 180:
                        print "Suggesting left for food"
                        suggestAction = ("turnRight", turnSpeed)
                    else:
                        print "Suggesting right for food"
                        suggestAction = ("turnLeft", turnSpeed)
                else:
                    print "Going to food!"
                    
                    if distToFood > DIST_THRESH:
                        if distToFood < DIST_NEAR:
                            speed = 2
                        else:
                            speed = 5
                        suggestAction = ("goStraight", speed)
                        extra_sleep += 0.1
                    else:
                        #Detect that we have picked up the food here.
                        if self.reactive.sensors.haveFood == True:
                            print "Food!!!"
                            self.reactive.sensors.haveFood = False
                            self.serial.write('D,0,0\n')
                            self.serial.readline()
                            TURNING_TOWARDS_HOME = True
                            GOING_TOWARDS_FOOD = False

                prevDistToFood = distToFood

            if TURNING_TOWARDS_HOME:
                #self.serial.write('D,0,0\n')
                #self.serial.readline()
                #time.sleep(0.1)
                self.reactive.sensors.updateModel()
                self.reactive.sensors.updatePos()
                angle = (180-robot.reactive.sensors.getAngleToHome())%360
                other_angle = 360-angle
                print "Turning towards home angle is " + str(angle) + " other one is " + str(other_angle)


                distToHome = self.reactive.sensors.getDistanceFromHome()

                if distToHome < DIST_NEAR and distToHome > prevDistToHome:
                    print "Home!!!"
                    self.serial.write('D,0,0\n')
                    self.serial.readline()
                    for i in range(6):
                        time.sleep(0.3)
                        self.serial.write('L,1,2\n')
                        self.serial.readline()
                        self.serial.write('L,0,2\n')
                        self.serial.readline()
                    #Drop off any food that we might have
                    self.reactive.sensors.haveFood = False
                    TURNING_TOWARDS_HOME = False
                    GOING_TOWARDS_FOOD = True

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
                    
                    if distToHome > DIST_THRESH:
                        if distToHome < DIST_NEAR:
                            speed = 2
                        else:
                            speed = 5
                        suggestAction = ("goStraight", speed)
                        extra_sleep += 0.1
                    else:
                        print "Home!!!"
                        self.serial.write('D,0,0\n')
                        self.serial.readline()
                        #Flash LED lights here.
                        #Change state 6 times which equals to flashing three times
                        for i in range(6):
                            time.sleep(0.3)
                            self.serial.write('L,1,2\n')
                            self.serial.readline()
                            self.serial.write('L,0,2\n')
                            self.serial.readline()
                        #Drop off any food that we might have
                        self.reactive.sensors.haveFood = False
                        TURNING_TOWARDS_HOME = False
                        GOING_TOWARDS_FOOD = True
                        

                prevDistToHome = distToHome
            self.reactive.act(suggestAction)
            time.sleep(perceive_speed + extra_sleep)
            print "Distance from home " + str(self.reactive.sensors.getDistanceFromHome())
            print "Angle from home " + str(self.reactive.sensors.getAngleFromHome())
            #If in initial roaming state, switch to Going_HOME state when we find our food.
            if not TURNING_TOWARDS_HOME and not GOING_TOWARDS_FOOD:
                if self.reactive.sensors.haveFood == True:
                    self.serial.write('D,0,0\n')
                    self.serial.readline()
                    TURNING_TOWARDS_HOME = True
                    perceive_speed = DEFAULT_SPEED_HOME
            #pygame.display.update()
            #clock.tick(20) # run 20 times per second, roughly 50ms
 
    def stop(self):
        self.serial.write('D,0,0\n')
        self.serial.readall()

def stop():
    serial.write('D,0,0\n')
    serial.readall()

robot = Robot()
