import math
from math import sqrt

class SensorModel:
    def __init__(self, s):
        self.s = s
        self.array = []
        self.prevMotorLeftPos = self.prevMotorRightPos = 0
        self.prevMotorLeftPos2 = self.prevMotorRightPos2 = 0
        self.phi = self.y = self.x = 0
        self.resetCounts()
        self.R = 13.1
        self.historyPosX = [0]
        self.historyPosY = [0]
    
    def resetCounts(self):
        self.s.write('G,0,0\n')
        self.s.readline()    

    def updatePos(self):
        (lDelta, rDelta) = self.calcOffsets()
        self.phi = self.phi - 0.5*(lDelta - rDelta)/(2*self.R)
        self.x = self.x + 0.5*(lDelta + rDelta)*math.cos(self.phi)
        self.y = self.y + 0.5*(lDelta + rDelta)*math.sin(self.phi)
        self.historyPosX += [self.x]
        self.historyPosY += [self.y]
        print "updatePos " + str(self.phi) + " " + str(self.x) + " " + str(self.y);

    def getDistanceFromHome(self):
        return sqrt(self.x**2+self.y**2)

    def getStartingAngle(self):
        return math.degrees(self.phi)%360

    def getAngleFromHome(self):
        d = self.getDistanceFromHome()
        if d == 0:
            alpha = 0
        else:
            alpha = math.acos(self.x/d)
        return math.degrees(alpha)%360

    def getAngleToHome(self):
        return (self.getAngleFromHome() + self.getStartingAngle()) % 360

    def calcOffsets(self):
        s = self.s
        s.write('H\n')
        st = s.readline()

        motorLeftPos, motorRightPos = map(int, st[2:].split(','))

        print "prevMotorPos" + str(self.prevMotorLeftPos2) + " " + \
                str(self.prevMotorRightPos2)        
        print "motorPos " + str(motorLeftPos) + " " + str(motorRightPos)

        offsetL = motorLeftPos - self.prevMotorLeftPos2
        offsetR = motorRightPos - self.prevMotorRightPos2

        self.prevMotorLeftPos2 = motorLeftPos
        self.prevMotorRightPos2 = motorRightPos

        print "offsets " + str(offsetL) + " " + str(offsetR)
        return (offsetL*0.08, offsetR*0.08)

    def calcDist(self):
        s = self.s
        s.write('H\n')
        st = s.readline()

        motorLeftPos, motorRightPos = map(int, st[2:].split(','))

        print "prevMotorPos" + str(self.prevMotorLeftPos) + " " + \
                str(self.prevMotorRightPos)        
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


        self.s.write('N\n')
        line = self.s.readline()
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
        elif sensorvalue < 150:
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
        elif sensorvalue < 150:
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
        elif sensorvalue < 150:
            toret = 4
        elif sensorvalue < 200:
            toret = 3
        elif sensorvalue < 300:
            toret = 2
        else:
            toret = 1

        print "sensefrontdist " + str(toret)

        return toret


