# -*- coding: utf-8 -*-
# export PYTHONPATH=$PYTHONPATH:~/Downloads/python/
import serial
import time
from math import sqrt

WALLTRESH = 70

s = serial.Serial('/dev/ttyS0')

moveright = [4, 5, 6]
moveleft = [0, 1, 7]
moveforward = [2, 3]

speedleft = 10
speedright = 10

xk = 0
prevPosL = prevPosR = 0

def start():
      while (True):
        s.write('N\n')
        line = s.readline()
        print line
        array = map(int, line[2:].split(','))
        array[-1] = array[-1] - 200
        ind = array.index(max(array))
        m = max(array)
        print "MAX " + str(m)
        if m < TRESH:
            s.write('D,10,10\n')
            s.readline()
        else:
            s.write('D,0,0\n')
            s.readline()
        #mean = float(sum(array))/len(array) if len(array) > 0 else float('nan')
        #print "Mean is " + str(mean)
        #print str(ind) + " " + str(array[ind])
        time.sleep(0.01)


def stop():
    s.write('D,0,0\n')
    s.readall()


def senseleft(arr):
    return (arr[0] + arr[1])/2


def sensefront(arr):
    return (arr[2] + arr[3])/2


def senseright(arr):
    return (arr[4] + arr[5])/2


def senseleftTest():
    s.write('N\n')
    line = s.readline()
    array = map(int, line[2:].split(','))
    array[-1] = array[-1] - 200
    return (array[0] + array[1])/2


def senserightTest():
    s.write('N\n')
    line = s.readline()
    array = map(int, line[2:].split(','))
    array[-1] = array[-1] - 200
    return (array[4] + array[5])/2


def sensefrontTest():
    s.write('N\n')
    line = s.readline()
    array = map(int, line[2:].split(','))
    array[-1] = array[-1] - 200
    return (array[2] + array[3])/2


prevright = 0;
prevleft = 0


def followWall():
    global speedright
    global speedleft
    global prevleft
    global prevright
    global s

    while (True):
        if abs(speedright > 15) or abs(speedleft > 15):
            speedright = 10
            speedleft = 10
        s.write('N\n')
        line = s.readline()
        print line
        array = map(int, line[2:].split(','))
        array[-1] = array[-1] - 200

        # First iteration, set value
        if prevleft == 0 or prevright == 0:
            prevleft = senseleft(array)
            prevright = senseright(array)

        if sensefront(array) < 90 and senseleft(array) < 90 and senseright(array) < 90:
            #Path ahead is clear!
            moveahead(10)
        elif sensefront(array) < 150:
            #Path ahead of us is clear, we can move, but we are near a wall and should try to keep there
            speedleft = abs(speedleft)
            speedright = abs(speedright)
            if senseleft(array) > 70 and senseleft(array) < 150:
                #If we are next to a all
                if abs(senseleft(array) - prevleft) < 10:
                    #If we are not moving closer to the wall
                    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
                    s.readline()
                else:
                    speedleft = speedleft + 1
                    speedright = speedright - 1
                    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
                    s.readline()
            elif senseright(array) > 70 and senseright(array) < 150:
                #Same but for a right wall
                if abs(senseright(array) - prevright) < 10:
                    #If we are not moving closer to the wall
                    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
                    s.readline()
                else:
                    speedleft = speedleft - 1
                    speedright = speedright + 1
                    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
                    s.readline()
            elif senseleft(array) > 150:
                #Too close to the wall, avoid
                speedleft = speedleft + 2
                speedright = speedright - 2
                s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
                s.readline()
            else:
                speedleft = speedleft - 2
                speedright = speedright + 2
                s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
                s.readline()

        else:
            #Path ahead is not clear, try to turn until it is, turn
            if speedleft > 0 and speedright > 0:
                #Change direction if necessary
                speedleft = -speedright
            s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
            s.readline()
        time.sleep(0.1)


#Movement functions
def curveright(value, speed):


    speedleft = speed - value
    speedright = speed + value
    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
    s.readline()


def curveleft(value, speed):

    speedleft = speed + value
    speedright = speed - value
    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
    s.readline()


def moveahead(value):
    global speedleft
    global speedright

    speedright = value
    speedleft = value

    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
    s.readline()


def movemaintainspeeds():
    global speedleft
    global speedright

    s.write('D,' + str(speedleft) + ',' + str(speedright) + '\n')
    s.readline()


def rotate(senseleft, senseright):
    #Sense direction with least obstacles and rotate there:
    if senseleft > senseright:
        s.write('D,4,-4\n')
        s.readline()
    else:
        s.write('D,-4,4\n')
        s.readline()
    time.sleep(0.2)


def followWall2():
    global speedright
    global speedleft
    global prevleft
    global prevright
    global s

    while (True):
        if abs(speedright > 15) or abs(speedleft > 15):
            speedright = 10
            speedleft = 10
        s.write('N\n')
        line = s.readline()
        print line
        array = map(int, line[2:].split(','))
        array[-1] = array[-1] - 200

        # First iteration, set value
        if prevleft == 0 or prevright == 0:
            prevleft = senseleft(array)
            prevright = senseright(array)

        if sensefront(array) < 110 and senseleft(array) < 110 and senseright(array) < 110:
            #Path ah1ead is clear!
            moveahead(10)
        elif senseleft(array) > 90 and sensefront(array) < 90:
            #We are near a wall
            if senseleft(array) > 350:
                #We will bump into a wall, move back!s
                curveleft(5)
            elif senseleft(array) > 250:
                curveright(2)
            elif senseleft(array) < 120:
                curveleft(2)
            else:
                moveahead(10)
        elif senseright(array) > 90 and sensefront(array) < 90:
            #We are near a wall
            if senseright(array) > 350:
                #We will bump into a wall, move back!s
                curveright(5)
            elif senseright(array) > 250:
                curveleft(2)
            elif senseright(array) < 120:
                curveright(2)
            else:
                moveahead(10)
        else:
            #Path ahead is not clear, try to turn until it is, turn
            rotate(senseleft(array), senseright(array))
        time.sleep(0.05)

class SensorModel:
    def SensorModel(self, s):
        self.s = s
        self.array = []

    def updateModel(self): #, dT):
        #Previous senses
        if len(self.array) != 0:
            self.prevleft = self.senseleftdist()
            self.prevright = self.senserightdist()
            self.prevfront = self.sensefrontdist()
        else:
            self.prevleft = 5
            self.prevright = 5
            self.prevfront = 5

        s.write('N\n')
        line = s.readline()
        print line
        try:
            array = map(int, line[2:].split(','))
            ok = True
        except: 
            self.updateModel()
            ok = False
        if not ok:
            return

        array[-1] = array[-1] - 200
        self.array = array; #Sensor array
        #speed = self.senseLeft() - self.left
        #self.left = self.left + speed * dT + K * (self.senseleft() - self.left - speed * dT);

    def senseleft(self):
        #Weight the sensor to the side more
        return int((self.array[0]*1.2 + self.array[1]*0.8)/2)


    def sensefront(self):
        #Weight the sensor to the side more
        return (self.array[2] + self.array[3])/2


    def senseright(self):
        #Weight the sensor to the side more
        return int((self.array[4]*0.8 + self.array[5]*1.2)/2)

    def senseleftdist(self):
        #Weight the sensor to the side more
        sensorvalue = self.senseleft()
        if sensorvalue <= 100:
            return 5; #Nothing near 3 sm of us
        elif sensorvalue > 100 and sensorvalue <= 120:
            return 4;
        elif sensorvalue > 120 and sensorvalue <= 140:
            return 3;
        elif sensorvalue > 120 and sensorvalue <= 140:
            return 2;
        else:
            return 1


    def sensefrontdist(self):
        #Weight the sensor to the side more
        sensorvalue = self.sensefront()
        if sensorvalue <= 100:
            return 5; #Nothing near 3 sm of us
        elif sensorvalue > 100 and sensorvalue <= 120:
            return 4;
        elif sensorvalue > 120 and sensorvalue <= 140:
            return 3;
        elif sensorvalue > 120 and sensorvalue <= 140:
            return 2;
        else:
            return 1


    def senserightdist(self):
        #Weight the sensor to the side more
        sensorvalue = self.senseright()
        if sensorvalue <=100:
            return 5; #Nothing near 3 sm of us
        elif sensorvalue > 100 and sensorvalue <= 120:
            return 4;
        elif sensorvalue > 120 and sensorvalue <= 140:
            return 3;
        elif sensorvalue > 120 and sensorvalue <= 140:
            return 2;
        else:
            return 1

class SensorModel1:
    def __init__(self, s):
        self.s = s
        self.array = []
        self.prevMotorLeftPos = self.prevMotorRightPos = 0

    def calcSpeed(self):
        s.write('H\n')
        st = s.readline()

        motorLeftPos, motorRightPos = map(int, st[2:].split(','))

        
        print "motorPos " + str(motorLeftPos) + " " + str(motorRightPos)

        speed = sqrt((motorLeftPos - self.prevMotorLeftPos)**2
                        + (motorRightPos - self.prevMotorRightPos)**2)

        print "speed " + str(speed)

        self.prevMotorLeftPos = motorLeftPos
        self.prevMotorRightPos = motorRightPos

        return speed

    def updateModel(self): #, dT):
        #Previous senses
#        if len(self.array) != 0:
#            prevleft = self.senseleftdist()
#            prevright = self.senserightdist()
#            prevfront = self.sensefrontdist()
#        else:
#            prevleft = 5
#            prevright = 5
#            prevfront = 5


        s.write('N\n')
        line = s.readline()
        print line
        try:
            array = map(int, line[2:].split(','))
            ok = True
        except: 
            self.updateModel()
            ok = False
        if not ok:
            return

        array[-1] = array[-1] - 200
        self.array = array; #Sensor array


        speed = self.calcSpeed()
        #speed = self.senseLeft() - self.left
        #self.left = self.left + speed * dT + K * (self.senseleft() - self.left - speed * dT);

    def senseleft(self):
        #Weight the sensor to the side more
        return int((self.array[0]*1.2 + self.array[1]*0.8)/2)
#        return int(self.array[0])


    def sensefront(self):
        return (self.array[2] + self.array[3])/2


    def senseright(self):
        return int((self.array[4]*0.8 + self.array[5]*1.2)/2)
        #return int(self.array[5])

    def getMaxSensor(self):
        val = max(self.array)
        ind = self.array.index(val)
        return (val, ind)

    def getMinSensor(self):
        val = min(self.array)
        ind = self.array.index(val)
        return (val, ind)

    def senseleftdist(self):
        sensorvalue = self.senseleft()
        toret = 5
        if sensorvalue <= 100:
            toret = 5
        elif sensorvalue < 120:
            toret = 4
        elif sensorvalue < 200:
            toret = 3
        elif sensorvalue < 300:
            toret = 2
        else:
            toret = 1

        print "senseleftdist " + str(toret)

        return toret

    def senserightdist(self):
        sensorvalue = self.senseright()
        toret = 5
        if sensorvalue <= 100:
            toret = 5
        elif sensorvalue < 120:
            toret = 4
        elif sensorvalue < 200:
            toret = 3
        elif sensorvalue < 300:
            toret = 2
        else:
            toret = 1

        print "senserightdist " + str(toret)

        return toret



    def sensefrontdist(self):
        sensorvalue = self.sensefront()
        toret = 5
        if sensorvalue <= 100:
            toret = 5
        elif sensorvalue < 120:
            toret = 4
        elif sensorvalue < 200:
            toret = 3
        elif sensorvalue < 300:
            toret = 2
        else:
            toret = 1

        print "sensefrontdist " + str(toret)

        return toret

sensor = SensorModel1(s)

def followWall3():
    global speedright
    global speedleft
    global prevleft
    global prevright
    global s
    global sensor

    while (True):
        if abs(speedright > 15) or abs(speedleft > 15):
            speedright = 10
            speedleft = 10
        sensor.updateModel()



        if sensor.sensefrontdist() >= 4 and sensor.senseleftdist() >= 4 and sensor.senserightdist() >= 4:
            print "forward"
            #Path ah1ead is clear!
            if sensor.prevleft < 4 and sensor.prevleft > 2:
                #We were near a wall, try to return closer
                curveleft(1);
            elif sensor.prevright < 4 and sensor.prevright > 2:
                #We were near a wall, try to return closer
                curveright(1);
            else:
                moveahead(10)
        elif sensor.senseleftdist() <= 4 and sensor.sensefrontdist() >= 4 and sensor.senseleftdist > 2:
            print "leftwall"
            #We are near a wall
            if sensor.senseleftdist() < 2:
                #We will bump into a wall, move back!s
                curveleft(5)
            elif sensor.senseleftdist() < 3:
                curveright(1)
            elif sensor.senseleftdist() > 3:
                curveleft(1)
            else:
                moveahead(10)
        elif sensor.senserightdist() <= 4 and sensor.sensefrontdist() >= 4 and sensor.senserightdist > 2:
            print "rightwall"
            #We are near a wall
            if sensor.senserightdist() < 2:
                #We will bump into a wall, move back!s
                curveright(5)
            elif sensor.senserightdist() < 3:
                curveleft(1)
            elif sensor.senserightdist() > 3:
                curveright(1)
            else:
                moveahead(10)
        else:
            #Path ahead is not clear, try to turn until it is, turn
            print "rotate"
            rotate(sensor.senseleft, sensor.senseright)
        time.sleep(0.05)

def followWall4():
    speed = 8 
    keepdist = 3
    near = 3
    sensor.updateModel()
    prevleft = sensor.senseleftdist() 
    followWallOnLeft = followWallOnRight = False
    roam = True
    turnUntilNear = False 
    turnedLeftCount = turnedRightCount = 0
    roamCount = 5
    spinCount = 20
    while(True):
        sensor.updateModel()
        left = sensor.senseleftdist()
        right = sensor.senserightdist()
        front = sensor.sensefrontdist()
        if (front <= keepdist and left <= keepdist and right <= keepdist) or\
        (left<=keepdist and right <= keepdist):
            deadend = True
        else: 
            deadend = False

        if deadend:
            print("We are in a dead end! Rotate away!")
            rotate(sensor.senseleft(), sensor.senseright())
            time.sleep(0.5)
        elif not turnUntilNear and front <= keepdist or left <= keepdist or right <= keepdist:
            print "something in front! " + str(left) + ' ' + str(right)
          # follow wall pick side with more opportunity (les ir light)
            if left <= right:
                print "choosing to go right!"
                followWallOnLeft = True
                followWallOnRight = False
                turnUntilNear = True
            else:
                print "choosing to go left!"
                followWallOnRight = True
                followWallOnLeft = False
                turnUntilNear = True
        elif roam:
            print "Roaming!"
            #_, ind = sensor.getMaxSensor()
            #if ind in moveleft:
            #    curveleft(1, speed)
            #    time.sleep(0.5)
            #    moveahead(speed) 
            #elif ind in moveright:
            #    curveright(1, speed)
            #    time.sleep(0.5)
            #    moveahead(speed) 
            #else:
            moveahead(speed) 
        else:
            print "dunno what to do"
       
        if followWallOnLeft:
           print "Following wall on the left"
           if turnUntilNear:
                print "Turning until near"
                if left <= near and front > near:
                    turnUntilNear = False
                else:
                    turnRight(speed)
           if not turnUntilNear:
               if left > keepdist:
                    if turnedLeftCount > roamCount:
                        print "Roaming!"
                        roam = True
                        followWallOnLeft = False
                        followWallOnRight = False
                        turnedLeftCount = 0
                    else:
                        turnedLeftCount += 1
                        moveLeft(speed)
                        print "Turned left for " + str(turnedLeftCount)
                    turnedRightCount=0
               elif left < keepdist:
                    if turnedRightCount > spinCount:
                        print "Roaming!"
                        roam = True
                        followWallOnRight = False
                        followWallOnLeft = False
                        turnedRightCount = 0
                    else:
                        turnedRightCount += 1
                        moveRight(speed)
                        print "Turned right for " + str(turnedRightCount)
                    turnedLeftCount=0
               else:
                    moveahead(speed)
          
        elif followWallOnRight:
           print "Following wall on the right"
           if turnUntilNear:
                print "Turning until near"
                if right <= near and front > near:
                    turnUntilNear = False
                else:
                    turnLeft(speed)
           if not turnUntilNear:
               if right > keepdist:
                    if turnedRightCount > roamCount:
                        print "Roaming!"
                        roam = True
                        followWallOnRight = False
                        followWallOnLeft = False
                        turnedRightCount = 0
                    else:
                        turnedRightCount += 1
                        moveRight(speed)
                        print "Turned right for " + str(turnedRightCount)
                    turnedLeftCount = 0
               elif right < keepdist:
                    if turnedLeftCount > spinCount:
                        print "Roaming!"
                        roam = True
                        followWallOnLeft = False
                        followWallOnRight = False
                        turnedLeftCount = 0
                    else:
                        turnedLeftCount += 1
                        moveLeft(speed)
                        print "Turned left for " + str(turnedLeftCount)
                    turnedRightCount=0
               else: 
                    moveahead(speed)
        time.sleep(0.05)
       ##if getch() == 's':
       ##     stop()
       ##     break       

       #prevleft = left

def moveLeft(value):
    print "moveLeft"
    s.write('D,0,' + str(value) +' \n')
    s.readline()

def moveRight(value):
    print "moveRight"
    s.write('D,' + str(value) + ',0\n')
    s.readline()


def turnLeft(value):
    print "turnLeft"
    s.write('D,' + str(-value) + ',' + str(value) + '\n')
    s.readline()



def turnRight(value):
    print "turnRight"
    s.write('D,' + str(value) + ',' + str(-value) + '\n')
    s.readline()

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
