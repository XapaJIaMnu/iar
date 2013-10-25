import math
from math import sqrt

class SensorModel:
    def __init__(self, s):
        self.s = s
        self.array = []
        self.lightarray = []
        self.prevMotorLeftPos = self.prevMotorRightPos = 0
        self.prevMotorLeftPos2 = self.prevMotorRightPos2 = 0
        self.phi = self.y = self.x = 0
        self.foodX = self.foodY = self.foodPhi = 0
        self.haveFood = False
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
        print "updatePos " + str(self.phi) + " " + str(self.x) + " " + str(self.y)

        #After updating position we should check for food
        if self.isFood():
            #If we have food, set that we picked it up and we should go home now
            self.haveFood = True
            self.foodX = self.x
            self.foodY = self.y
            self.foodPhi = self.phi

    def getDistanceFromHome(self):
        return sqrt(self.x**2+self.y**2)

    def getStartingAngle(self):
        print "Starting angle is " + str(math.degrees(self.phi))
        print "Starting angle is " + str(math.degrees(self.phi)%360)
        return math.degrees(self.phi)%360

    def getAngleFromHome(self):
        d = self.getDistanceFromHome()
        if d == 0:
            alpha = 0
        else:
            alpha = math.acos(self.x/d)
        if self.y > 0:
            alpha = -alpha
        print "Angle from home is " + str(math.degrees(alpha)%360)
        return math.degrees(alpha)%360

    def getAngleToHome(self):
        return (self.getAngleFromHome() + self.getStartingAngle()) % 360

    #Same functions, but for food
    def getDistanceFromFood(self):
        return sqrt((self.x - self.foodX)**2+(self.y - self.foodY)**2)

    def getFoodStartingAngle(self):
        print "Starting food angle is " + str(math.degrees(self.foodPhi))
        print "Starting food angle is " + str(math.degrees(self.foodPhi)%360)
        return math.degrees(self.phi)%360

    def getAngleFromFood(self):
        d = self.getDistanceFromFood()
        if d == 0:
            alpha = 0
        else:
            alpha = math.acos(self.x/d)
        if self.y > 0:
            alpha = -alpha
        print "Angle from food is " + str(math.degrees(alpha)%360)
        return math.degrees(alpha)%360

    def getAngleToFood(self):
        return (self.getAngleFromFood() + self.getFoodStartingAngle()) % 360

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

        #Read proximity sensors
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

        self.getLightSensors();

        #speed = self.senseLeft() - self.left
        #self.left = self.left + speed * dT + K * (self.senseleft() - self.left - speed * dT);

    def getLightSensors(self):
        #Read light sensors
        self.s.write('O\n')
        lightline = self.s.readline()
        print "Light sensors: " + str(lightline)

        try:
            array = map(int, lightline[2:].split(','))
            ok = True
        except: 
            self.getLightSensors()
            ok = False
        if not ok:
            return

        self.lightarray = array

    #Find out where there is food at our current position.
    #Need to calibrate the lightarray value
    def isFood(self):
        if (self.enseleftdist() == 1) and (self.senserightdist() == 1) and (self.sensefrontdist() == 1) and sum(self.lightarray) > 2000:
            return True;
        else:
            return False;


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
        if sensorvalue <= 120:
            toret = 5
        elif sensorvalue < 140:
            toret = 4
        elif sensorvalue < 180:
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
        if sensorvalue <= 120:
            toret = 5
        elif sensorvalue < 140:
            toret = 4
        elif sensorvalue < 180:
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
        if sensorvalue <= 120:
            toret = 5
        elif sensorvalue < 140:
            toret = 4
        elif sensorvalue < 180:
            toret = 3
        elif sensorvalue < 300:
            toret = 2
        else:
            toret = 1

        print "sensefrontdist " + str(toret)

        return toret


