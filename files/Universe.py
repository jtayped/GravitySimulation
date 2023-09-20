from .config.constants import *
from .elements.Mass import Mass
import pygame, sys

class Universe:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        self.gameOver = False

        self.masses = []
        #self.masses.append(Mass(1*1000, 10, (WIDTH//5, HEIGHT//5), (2.9*10, -1.5*10)))
        self.masses.append(Mass(1*1000, 10, (WIDTH//5, HEIGHT//5), (2.9*10, -1.5*10)))
        self.masses.append(Mass(15*100000, 30, (WIDTH//2, HEIGHT//2)))

    def updateMasses(self):
        for mass in self.masses:
            mass.update(self.screen, self.masses)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.masses.append(Mass(1*1000, 10, (x, y), (2.5, -2)))

    def update(self):
        self.events()
        self.screen.fill(BACKGROUND_COLOR)

        # GAME #

        self.updateMasses()

        ########

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while not self.gameOver:
            self.update()
