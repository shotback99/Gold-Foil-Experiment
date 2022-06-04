from math import pi, radians, cos, sin
import pygame
# do i have to do init

class Electron:
    def __init__(self, angle, distance, nucleus_center, turn):
        self.angle = angle
        self.distance = distance
        self.nucleus_center = nucleus_center
        self.size = 4
        self.turn = turn
        self.in_shell = True
        self.orbital_velocity = (2*pi*self.distance)/(360/self.turn)
        self.vx, self.vy = (0, 0)
        self.position = self.calculate_pos()

    # def upd_velocity(self, alpha_spd):
    #     a = radians(self.angle) # math module by default uses radians
    #     x = self.orbital_velocity * cos(a)
    #     y = self.orbital_velocity * sin(a)
    #     self.vx, self.vy = x, y

    def calculate_pos(self):
        if self.in_shell:
            a = radians(self.angle) # math module by default uses radians
            x = self.distance * cos(a)
            y = self.distance * sin(a)
            x += self.nucleus_center[0]
            y += self.nucleus_center[1]
            return (x, y)
        else:
            x = self.position[0] + self.vx
            y = self.position[1] + self.vy
            return (x, y)
    def draw(self, screen): # also updates speed
        self.position = self.calculate_pos()
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.size)
        self.angle += self.turn # -1 or 1 , (2 * pi * r)/ t
