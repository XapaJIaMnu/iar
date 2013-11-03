import math
import numpy as np

SCALE = 0.03 

class Particle:
    def __init__(self, particle=None):
        if particle != None:
            self.phi = particle.phi
            self.x = particle.x
            self.y = particle.y
        else:
            self.phi = self.x = self.y = self.p = 0
            self.x = 500*1.5
            self.y = 260*1.5


class Particles:
    def __init__(self, number, mapReader):
        self.mapReader = mapReader
        self.num = number
        self.particles = [Particle() for _ in range(number)]

    def doPrediction(self, lDelta, rDelta, R):
        global SCALE

        particles = self.particles

        for particle in particles:
            particle.phi = particle.phi - 0.5*(lDelta - rDelta)/(2*R)
            # add gaussian noise with standard diviation SCALE
            particle.phi += np.random.normal(scale=SCALE)
            particle.x = particle.x + 0.5*(lDelta + rDelta)*math.cos(particle.phi)
            particle.y = particle.y + 0.5*(lDelta + rDelta)*math.sin(particle.phi)

    def doCorrection(self, sensorsFrontLeftRightDist):
        particles = self.particles
        normP = 0
        for particle in particles:
            # TODO check map for probability of current sensor readings
            # ex particle.p = map.getP((particle.x, particle.y, particle.phi), sensors)
            mapX, mapY =  robotToMap(particle.x, particle.y)
            if self.mapReader.impossible(mapX, mapY):
                particle.p = 0
            else:
                particle.p = getProb(self.mapReader.getNearbyWalls(mapX, mapY, particle.phi), sensorsFrontLeftRightDist)
            
            # dummy p
            #particle.p = 1

            normP = normP + particle.p

        n = len(particles)

        sample = np.random.random_sample(n) 

        newParticles = []
        self.particlesX = []
        self.particlesY = []

        if normP == 0:
            # all the particle positions are impossible
            self.particles = self.prevParticles
            return

        for prob in sample:
            accumProb = 0
            current = 0

            while accumProb < prob and current < n:
                accumProb += float(particles[current].p) / normP
                current += 1
            #print "Picking", current-1, particles[current-1].x, particles[current-1].y, particles[current-1].phi, particles[current-1].p
            newParticles.append(Particle(particles[current-1]))
            self.particlesX.append(particles[current-1].x)
            self.particlesY.append(particles[current-1].y)
            
        assert len(newParticles) == len(particles)
    
        self.prevParticles = self.particles

        self.particles = newParticles

    def getMeanPos(self):
        particles = self.particles

        meanX = 0
        meanY = 0
        meanPhi = 0
        n = float(len(particles))

        for particle in particles:
            meanX += particle.x
            meanY += particle.y
            meanPhi += particle.phi

        return (meanPhi / n, meanX / n, meanY / n)

def getProb(mapDist, sensorsDist):
    #print mapDist
    #print sensorsDist
    frontP = mapDist[0]/float(sensorsDist[0])
    if frontP > 1:
        frontP = 1 / frontP
    leftP = mapDist[1]/float(sensorsDist[1])
    if leftP > 1:
        leftP = 1 / leftP
    rightP = mapDist[2]/float(sensorsDist[2])
    if rightP > 1:
        rightP = 1 / rightP
    
    #print "Particle probs ", frontP, leftP, rightP

    return (frontP + leftP + rightP)/3

def robotToMap(x, y):
   return (x/1.5, 533-y/1.5)


