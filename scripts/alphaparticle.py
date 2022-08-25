from random import uniform
from math import sqrt
import pygame
class AlphaParticle:
    def __init__(self, pos, size = 5, colour = (255, 0, 255)):
        self.position = pos
        self.velocity = [0, uniform(-5, -10)]
        self.size = size
        self.colour = colour
        self.in_bounds = True
        self.bounds = 5
        self.intensity = 1

    def check_bounds(self, electron_list):
        if len(electron_list) == 0: return []
        for electron in electron_list:
            ax, ay = electron.position
            alphax, alphay = self.position
            dist = sqrt((ax-alphax)**2 + (ay-alphay)**2)
            if dist <= self.bounds:
                electron.in_shell = False
                force = self.velocity#self.bounds*self.intensity
                if electron.position[0] < self.position[0]: x_force = -force[0]
                elif electron.position[0] > self.position[0]: x_force = -force[0] # this works
                else:
                    x_force = 0
                if electron.position[1] < self.position[1]: y_force = force[1]#
                elif electron.position[1] > self.position[1]: y_force = force[1]


                electron.vy += y_force #* (1/(dist**2)) # makes force too small
                electron.vx += x_force #* (1/(dist**2))
        return electron_list
    def draw(self, screen):
        #pygame.draw.circle(screen, (255, 255, 217), self.position, self.bounds)
        pygame.draw.circle(screen, self.colour, self.position, self.size)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
