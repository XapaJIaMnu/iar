import math
import numpy as np

SCALE = 1

class Particle:
    def __init__(self):
        self.phi = self.x = self.y = self.p = 0
        self.x = 500
        self.y = 260

class Particles:
    def __init__(self, number):
        self.num = number
        self.particles = [Particle() for _ in range(number)]

    def doPrediction(self, lDelta, rDelta, R):
        global SCALE

        particles = self.particles

        for particle in particles:
            particle.phi = particle.phi - 0.5*(lDelta - rDelta)/(2*R)
            # add gaussian noise with standard diviation SCALE
            #particle.phi += np.random.normal(scale=SCALE)
            particle.x = particle.x + 0.5*(lDelta + rDelta)*math.cos(particle.phi)
            particle.y = particle.y + 0.5*(lDelta + rDelta)*math.sin(particle.phi)

    def doCorrection(self, sensors):
        particles = self.particles
        normP = 0
        for particle in particles:
            # TODO check map for probability of current sensor readings
            # ex particle.p = map.getP((particle.x, particle.y, particle.phi), sensors)
            
            # dummy p
            particle.p = 1

            normP = normP + particle.p

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

            newParticles.append(particles[current-1])
            self.particlesX.append(particles[current-1].x)
            self.particlesY.append(particles[current-1].y)
            
        assert len(newParticles) == len(particles)

        particles = newParticles

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
