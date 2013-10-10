from math import sqrt

class SensorModel:
    def __init__(self, s):
        self.s = s
        self.array = []
        self.prevMotorLeftPos = self.prevMotorRightPos = 0

    def calcSpeed(self):
        s = self.s
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


