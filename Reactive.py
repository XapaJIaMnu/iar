import sensor_model
import time

speed = 8 
keepdist = 3
near = 3
followWallOnLeft = followWallOnRight = False
roam = True
turnUntilNear = False 
turnedLeftCount = turnedRightCount = 0
roamCount = 5
spinCount = 20


class Reactive:

    def __init__(self, serial):
        self.serial = serial
        self.sensors = sensor_model.SensorModel(self.serial)
    def act(self, controlSuggests):
        global speed
        global keepdist
        global near
        global followWallOnLeft
        global followWallOnRight
        global roam
        global turnUntilNear
        global turnedLeftCount
        global turnedRightCount
        global roamCount
        global spinCount
        self.sensors.updateModel()
        left = self.sensors.senseleftdist()
        right = self.sensors.senserightdist()
        front = self.sensors.sensefrontdist()
        if (front <= keepdist and left <= keepdist and right <= keepdist) or\
        (left<=keepdist and right <= keepdist):
            deadend = True
        else: 
            deadend = False

        if deadend:
            print("We are in a dead end! Rotate away!")
            self.rotate(self.sensors.senseleft(), self.sensors.senseright())
            time.sleep(0.5)
        elif not turnUntilNear and (front <= keepdist or left <= keepdist or right <= keepdist):
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
            self.moveahead(speed) 
        else:
            print "dunno what to do"
       
        if followWallOnLeft:
           print "Following wall on the left"
           if turnUntilNear:
                print "Turning until near"
                if left <= near and front > near:
                    turnUntilNear = False
                else:
                    self.turnRight(speed)
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
                        self.moveLeft(speed)
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
                        self.moveRight(speed)
                        print "Turned right for " + str(turnedRightCount)
                    turnedLeftCount=0
               else:
                    self.moveahead(speed)
          
        elif followWallOnRight:
           print "Following wall on the right"
           if turnUntilNear:
                print "Turning until near"
                if right <= near and front > near:
                    turnUntilNear = False
                else:
                    self.turnLeft(speed)
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
                        self.moveRight(speed)
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
                        self.moveLeft(speed)
                        print "Turned left for " + str(turnedLeftCount)
                    turnedRightCount=0
               else: 
                    self.moveahead(speed)

    def moveahead(self, value):
        self.serial.write('D,' + str(value) + ',' + str(value) + '\n')
        self.serial.readline()

    def rotate(self, senseleft, senseright):
    #Sense direction with least obstacles and rotate there:
        s = self.serial
        if senseleft > senseright:
            s.write('D,4,-4\n')
            s.readline()
        else:
            s.write('D,-4,4\n')
            s.readline()
        time.sleep(0.2)



    def moveLeft(self, value):
        print "moveLeft"
        self.serial.write('D,0,' + str(value) +' \n')
        self.serial.readline()

    def moveRight(self, value):
        print "moveRight"
        self.serial.write('D,' + str(value) + ',0\n')
        self.serial.readline()


    def turnLeft(self, value):
        print "turnLeft"
        self.serial.write('D,' + str(-value) + ',' + str(value) + '\n')
        self.serial.readline()


    def turnRight(self, value):
        print "turnRight"
        self.serial.write('D,' + str(value) + ',' + str(-value) + '\n')
        self.serial.readline()


