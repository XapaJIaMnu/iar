import math
import numpy as np
import scipy.stats

SCALE = 0.03 

class Particle:
    def __init__(self, particle=None, starting=False):
        if particle != None:
            self.phi = particle.phi
            self.x = particle.x
            self.y = particle.y
        elif starting:
            self.x = 500*1.5
            self.y = 260*1.5
            self.phi = 0
        else:
            self.phi = self.x = self.y = self.p = 0
            self.x = np.random.randint(800*1.5)
            self.y = np.random.randint(533*1.5)
            self.phi = np.random.random()*2*np.pi


class Particles:
    def __init__(self, number, mapReader):
        self.mapReader = mapReader
        self.num = number
        self.particles = [Particle(starting=True) for _ in range(number)]

    def doPrediction(self, lDelta, rDelta, R):
        global SCALE

        particles = self.particles

        for particle in particles:
            particle.phi = particle.phi - 0.5*(lDelta - rDelta)/(2*R)
            # add gaussian noise with standard diviation SCALE
            particle.phi += np.random.normal(scale=SCALE)
            
            if np.random.random() > 0.3:
                particle.prevx = particle.x
                particle.x = particle.x + 0.5*(lDelta + rDelta)*math.cos(particle.phi)
            if np.random.random() > 0.3:
                particle.prevy = particle.y
                particle.y = particle.y + 0.5*(lDelta + rDelta)*math.sin(particle.phi)

    def doCorrection(self, sensorsFrontLeftRightDist):
        particles = self.particles
        normP = 0
        for particle in particles:
            # TODO check map for probability of current sensor readings
            # ex particle.p = map.getP((particle.x, particle.y, particle.phi), sensors)
            mapX, mapY =  robotToMap(particle.x, particle.y)
            while self.mapReader.impossible(mapX, mapY):
                print "Impossible particle!"
                newParticle = Particle()
                particle.x, particle.y, particle.phi = newParticle.x, newParticle.y, newParticle.phi
                mapX, mapY =  robotToMap(particle.x, particle.y)
                
            particle.p = getProb(self.mapReader.getNearbyWalls(mapX, mapY, particle.phi), sensorsFrontLeftRightDist)
            
            # dummy p
            #particle.p = 1

            normP = normP + particle.p
        
        print "NORMP P P P ", normP

        if normP < 200:
           self.particles = [Particle() for _ in range(len(particles))]

        else:
            n = len(particles)

            sample = np.random.random_sample(n) 

            newParticles = []
            self.particlesX = []
            self.particlesY = []

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
    frontP = scipy.stats.norm(sensorsDist[0], 1).cdf(mapDist[0]) 
    leftP = scipy.stats.norm(sensorsDist[1], 1).cdf(mapDist[1]) 
    rightP = scipy.stats.norm(sensorsDist[2], 1).cdf(mapDist[2]) 
#    frontP = mapDist[0]/float(sensorsDist[0])
#    if frontP > 1:
#        frontP = 1 / frontP
#    leftP = mapDist[1]/float(sensorsDist[1])
#    if leftP > 1:
#        leftP = 1 / leftP
#    rightP = mapDist[2]/float(sensorsDist[2])
#    if rightP > 1:
#        rightP = 1 / rightP
#    
#    #print "Particle probs ", frontP, leftP, rightP
#
#    return (frontP + leftP + rightP)/3
    return frontP + leftP + rightP

def robotToMap(x, y):
   return (x/1.5, 533-y/1.5)


