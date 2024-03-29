import pygame
from pyautogui import size
from sys import exit
from random import randint, uniform, choice
from math import sqrt, ceil, cos, sin, radians, pi
import matplotlib.pyplot as plt

from alphaparticle import AlphaParticle
from atom import Atom

pygame.init()
pygame.display.set_caption("Gold Foil Experiment")

"""
make it more accurate
collect data
represent data

add main menu
"""

class Game:
    def __init__(self, WIDTH = 700, HEIGHT = 700, bg_colour = (217, 217, 217)):
        self.size = size()
        self.bg_colour = bg_colour
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.atoms = []
        self.alpha = []
        self.toggle_ui = 0
        pygame.time.set_timer(pygame.USEREVENT, 100)
        self.general_config = [1]
        self.general_electrons = []
        self.plot_alpha_pos = []

    def run(self):
        while True:
            self.screen.fill(self.bg_colour)
            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.atoms = []
                        self.plot_alpha_pos = []
                        self.general_config = [1]
                        self.toggle_ui = 0
                        self.general_electrons = []
                    if event.key == pygame.K_m:
                        self.display_data()
                    if event.key == pygame.K_SPACE:
                        self.toggle_ui += 1
                        self.toggle_ui %= 4 # resets to 0 at 4
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                if event.type == pygame.USEREVENT:
                    self.generate_alpha()
                mouse_pressed = pygame.mouse.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        atom = Atom(self.screen, m_pos, electron_config = self.general_config)
                        self.atoms.append(atom)
                    if event.button == 4:
                        for atom in self.atoms:
                            x = self.general_config.copy()
                            if len(x) == 0:
                                x.append(0)
                            elif x[-1] == 8 or (x[0] == 2 and len(x) == 1):
                                x.append(0)
                            x[-1] += 1

                            atom.electron_config = x
                            atom.shells = len(x)
                            atom.electrons = []
                            atom.create_electrons()
                            atom.upd_electron_pos()
                        self.general_config = x

                    if event.button == 5:
                        for atom in self.atoms:
                            x = self.general_config.copy()
                            if len(x) == 0:continue
                            x[-1] -= 1
                            if x[-1] == 0:
                                x.pop()
                            atom.electron_config = x
                            atom.shells = len(x)
                            atom.electrons = []
                            atom.create_electrons()
                            atom.upd_electron_pos()
                        self.general_config = x
                    self.general_electrons = [] # need to keep calling this to upd references to obj
                    for atom in self.atoms:
                        self.general_electrons.extend(atom.electrons)
            for atom in self.atoms:
                self.alpha = atom.check_bounds_2(self.alpha)
                #atom.position = m_pos
                #atom.upd_electron_pos()
            self.draw_atoms()

            for alpha in self.alpha:
                self.general_electrons = alpha.check_bounds(self.general_electrons)
                alpha.draw(self.screen)
                for electron in self.general_electrons:
                    if electron.position[1] < 0 - electron.size or electron.position[1] > self.size[1] + electron.size: self.general_electrons.remove(electron)
            pygame.display.update()
            self.clock.tick(60)
            for alpha in self.alpha: # alpha doesn't draw properly if not here
                self.last_alpha_pos(alpha)

    def last_alpha_pos(self, alpha):
        if -alpha.size > alpha.position[1] or alpha.position[1] > self.size[1]+alpha.size or -alpha.size > alpha.position[0] or alpha.position[0] > self.size[0]+alpha.size:
            pos = (alpha.position[0], alpha.position[1])
            self.plot_alpha_pos.append(pos)
            self.alpha.remove(alpha)
    def draw_atoms(self):
        if self.toggle_ui > 0:
            for atom in self.atoms: # displays bounds
                pygame.draw.circle(self.screen, (255, 255, 217), atom.position, atom.bounds)
        for atom in self.atoms:
            pygame.draw.circle(self.screen, atom.colour, atom.position, atom.size)
            # atom.random_movement()
            if self.toggle_ui == 2:
                atom.display_electrons()
            if self.toggle_ui > 2:
                atom.display_shells()
                atom.display_electrons()
    def generate_alpha(self):
            ran_x = randint(0, self.size[0])
            alpha = AlphaParticle((ran_x, self.size[1]))
            self.alpha.append(alpha)
    def display_data(self):# add some more use full stats
        """
        number of atoms:electrons:alpha particles
        where each alpha particle went
        most common direction with colour graph
        """
        offset = 50
        x = [i[0] for i in self.plot_alpha_pos]
        y = [i[1] for i in self.plot_alpha_pos]

        #f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        pygame.time.set_timer(pygame.USEREVENT, 0)

        plt.subplot(1, 2, 1)
        plt.xlim([-offset, self.size[0]+offset])
        plt.ylim(-offset, self.size[1]+offset)
        scatter = plt.scatter(x, y, c = [(1, 0, 0)], alpha = 0.1)
        scatter.axes.invert_yaxis()
        plt.title("direction alpha particles went")


        plt.subplot(1, 2, 2)
        langs = ["atoms", "alpha particles"]
        plt.bar(langs, [len(self.atoms), len(self.alpha)])
        plt.title("amount")

        plt.show()
        pygame.time.set_timer(pygame.USEREVENT, 100)
        plt.close("all")

# polar catesian conversian
#To convert from Polar Coordinates (r,θ) to Cartesian Coordinates (x,y) : x = r × cos( θ ) y = r × sin( θ )
if __name__ == "__main__":
    game = Game(WIDTH = 1918, HEIGHT = 1079, bg_colour =(0, 0, 0))
    game.run()
