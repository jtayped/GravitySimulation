from .config.constants import *
from .elements.Mass import Mass
import pygame, sys, math

class Universe:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        self.gameOver = False

        self.point1 = self.point2 = None

        self.masses = []
        self.masses.append(Mass(2.5e5, 10, (WIDTH*0.5, HEIGHT*0.5), movement=False))
        #self.masses.append(Mass(10e3, 5, (WIDTH*0.5, HEIGHT*0.75), (-2.605, 0)))
        self.masses.append(Mass(10e3, 5, (WIDTH*0.5125, HEIGHT*0.75), (-2.595, 0)))

    def handleCollisions(self, mass1: Mass, mass2: Mass):
        distance = mass2.position.distance_to(mass1.position)

        if distance < mass1.radius + mass2.radius:
            if mass1.mass > mass2.mass:
                # Calculate the new radius based on the volume ratio
                new_radius = ((mass1.volume() + mass2.volume()) / (4/3 * math.pi))**(1/3)
                
                # Update the velocity according to conservation of momentum
                mass1.speed = ((mass1.mass * mass1.speed) + (mass2.mass * mass2.speed)) / (mass1.mass + mass2.mass)
                
                # Update the mass and radius
                mass1.mass += mass2.mass
                mass1.radius = new_radius

                return mass2

            else:
                # Calculate the new radius based on the volume ratio
                new_radius = ((mass1.volume() + mass2.volume()) / (4/3 * math.pi))**(1/3)
                
                # Update the velocity according to conservation of momentum
                mass2.speed = ((mass1.mass * mass1.speed) + (mass2.mass * mass2.speed)) / (mass1.mass + mass2.mass)
                
                # Update the mass and radius
                mass2.mass += mass1.mass
                mass2.radius = new_radius

                return mass1

        return None

    def updateMasses(self):
        for mass in self.masses:
            mass.update(self.screen, self.masses)

        masses_to_remove = []  # Create a list to store masses to be removed
    
        for i in range(len(self.masses)):
            for j in range(i + 1, len(self.masses)):
                mass1 = self.masses[i]
                mass2 = self.masses[j]
                massToRemove = self.handleCollisions(mass1, mass2)

                if massToRemove is not None:
                    masses_to_remove.append(massToRemove)

        # Remove the masses that need to be removed
        for mass in masses_to_remove:
            self.masses.remove(mass)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.point1 = pygame.math.Vector2(x, y)

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                self.point2 = pygame.math.Vector2(x, y)
                
                dx = self.point1.x - self.point2.x
                dy = self.point1.y - self.point2.y

                speedX = dx/30
                speedY = dy/30

                self.masses.append(Mass(10e3, 5, self.point1, (-speedX, -speedY)))

                print("\nMass: 10e3", "Radis: 10", f"Pos: {self.point1}", f"Speed: {-speedX} / {-speedY}")
                self.point1 = self.point2 = None

    def update(self):
        self.events()
        self.screen.fill(BACKGROUND_COLOR)

        # GAME #

        if self.point1 is not None:
            x, y = pygame.mouse.get_pos()
            point2 = pygame.math.Vector2(x, y)

            if self.point1.distance_to(point2) != 0:
                # Calculate the direction vector from self.point1 to (x, y)
                directionVector = point2 - self.point1
                scaledVector = directionVector.normalize() * 1000
                endpoint = self.point1 + scaledVector

                pygame.draw.line(self.screen, 'green', point2, endpoint, 2)
                pygame.draw.circle(self.screen, 'white', point2, 3)

            pygame.draw.circle(self.screen, 'white', self.point1, 5)
            pygame.draw.line(self.screen, 'white', self.point1, point2, 2)

        self.updateMasses()

        ########

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while not self.gameOver:
            self.update()
