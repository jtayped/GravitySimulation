from ..config.constants import *
import pygame, math

class Mass:
    def __init__(
            self, mass: int, 
            radius: int, 
            pos: tuple, 
            speed=(0, 0),
            acceleration=(0, 0),
            color: str = 'white',
            movement=True
            ) -> None:
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.acceleration = acceleration
        self.color = color
        self.hasMovement = movement

        self.trajectory = []

        self.position = pygame.math.Vector2(
            pos[0], pos[1]
        )

        self.speed = pygame.math.Vector2(
            speed[0], speed[1]
        )
        self.acceleration = pygame.math.Vector2(
            acceleration[0], acceleration[1]
        )

    def volume(self):
        # Calculate and return the volume of the sphere
        return (4/3) * math.pi * (self.radius ** 3)
    
    def calculateGravitationalForce(self, otherMass) -> pygame.math.Vector2:
        # Calculate the distance between the two masses
        r = otherMass.position - self.position
        d = r.length()
        
        # Calculate force vector
        f = (GRAVITATIONAL_CONSTANT * self.mass * otherMass.mass) / (d ** 2)
        fVec = (f / d) * r.normalize()

        return fVec

    def movement(self, masses: list):
        # Calculate the interaction between masses
        self.total_force = pygame.math.Vector2(0, 0)
        for mass in masses:
            if mass is not self:
                force = self.calculateGravitationalForce(mass)
                self.total_force += force

        if self.hasMovement:
            # Modify the acceleration based on the total force
            self.acceleration = self.total_force / self.mass

            # Modify the position
            self.speed += self.acceleration
            self.position += self.speed

        self.trajectory.append(
            (self.position.x, self.position.y)
        )

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        
        if self.hasMovement and len(self.trajectory) > 2:
            if len(self.trajectory) > 200:
                self.trajectory.pop(0)

            pygame.draw.lines(screen, 'white', False, self.trajectory, 2)

    def update(self, screen: pygame.Surface, masses: list):
        self.movement(masses)
        self.draw(screen)

    def __repr__(self) -> str:
        return f'Mass: {self.mass} / Radius: {self.radius}'