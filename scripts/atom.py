import pygame
from random import uniform, choice
from math import sqrt
from electron import Electron
class Atom:
    def __init__(self, screen, pos, electron_config, size = 5, colour = (0, 0, 255, 100), bounds = 200):
        self.position = pos
        self.size = size
        self.bounds = bounds
        self.colour = colour
        self.alpha_in_bounds = []
        self.intensity = 5
        self.screen = screen
        self.electrons = []
        self.electron_config = electron_config
        self.shells = len(self.electron_config)
        self.turn = choice([-1, 1])
        self.create_electrons()
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.size)    

    def check_bounds(self, alpha_list):
        if len(alpha_list) == 0: return []
        for alpha in alpha_list:
            ax, ay = alpha.position
            atomx, atomy = self.position
            dist = sqrt((ax-atomx)**2 + (ay-atomy)**2)
            if dist <= self.bounds:
                if alpha.position[0] < self.position[0]: force = -self.bounds*self.intensity
                elif alpha.position[0] > self.position[0]: force = self.bounds*self.intensity

                y_force = self.bounds*self.intensity
                alpha.velocity[1] += y_force * (1/(dist**2))
                #force = 0
                alpha.velocity[0] += force * (1/(dist**2))
        return alpha_list

    def check_bounds_2(self, alpha_list):
        if len(alpha_list) == 0: return []
        for alpha in alpha_list:
            ax, ay = alpha.position
            atomx, atomy = self.position
            dist = sqrt((ax-atomx)**2 + (ay-atomy)**2)
            if dist <= self.bounds:
                force = self.bounds*self.intensity
                if alpha.position[0] < self.position[0]: x_force = -force
                elif alpha.position[0] > self.position[0]: x_force = force
                else:
                    x_force = 0
                if alpha.position[1] < self.position[1]: y_force = -force# check to see when it needs to be negative or could accidentally look like attraction
                elif alpha.position[1] > self.position[1]: y_force = force


                alpha.velocity[1] += y_force * (1/(dist**2))
                alpha.velocity[0] += x_force * (1/(dist**2))
        return alpha_list
    def random_movement(self):
        r_speed = 1
        self.position = (self.position[0] + uniform(-r_speed, r_speed), self.position[1] + uniform(-r_speed, r_speed))
        self.upd_electron_pos()
    def display_shells(self):
        for i in range(1, self.shells+1):
            pygame.draw.circle(self.screen, (0, 0, 0), self.position, (self.bounds/self.shells)*i, 1)
    def display_electrons(self):
        for electron in self.electrons:
            electron.draw(self.screen)
    def create_electrons(self):
        for i in range(0, self.shells):
            for j in range(self.electron_config[i]):

                distance = (self.bounds/self.shells)*(i+1) # distance from center based on max electrons in each shell
                angle = (360 / self.electron_config[i])*j # starts at angle 0

                obj = Electron(angle, distance, self.position, turn = self.turn)
                self.electrons.append(obj)
    def upd_electron_pos(self):
        distances = []
        angles = []
        for i in range(self.shells):
            for j in range(self.electron_config[i]):
                distance = (self.bounds/self.shells)*(i+1)
                angle = (360 / self.electron_config[i])*j
                distances.append(distance)
                angles.append(angle)
        for index, electron in enumerate(self.electrons):
            electron.distance = distances[index]
            electron.angle = angles[index]
            electron.nucleus_center = self.position
