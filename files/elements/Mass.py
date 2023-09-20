from ..config.constants import *
import pygame

class Mass:
    def __init__(
            self, mass: int, 
            radius: int, 
            pos: tuple, 
            speed=(0, 0),
            acceleration=(0, 0),
            color: str = 'white'
            ) -> None:
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.acceleration = acceleration
        self.color = color

        self.position = pygame.math.Vector2(
            pos[0], pos[1]
        )

        self.speed = pygame.math.Vector2(
            speed[0], speed[1]
        )
        self.acceleration = pygame.math.Vector2(
            acceleration[0], acceleration[1]
        )
        
    def calculateGravitationalForce(self, otherMass) -> pygame.math.Vector2:
        # Calculate the distance between the two masses
        r = otherMass.position - self.position
        d = r.length()
        
        # Calculate force vector
        f = (GRAVITATIONAL_CONSTANT * self.mass * otherMass.mass) / (d ** 2)
        fVec = (f / d) * r.normalize()

        return fVec

    def handle_collision(self, other_mass):
        # Check if the masses are colliding
        distance = self.position.distance_to(other_mass.position)
        if distance < self.radius + other_mass.radius:
            # Elastic collision formula
            relative_velocity = self.speed - other_mass.speed
            impulse = 2 * self.mass * other_mass.mass / (self.mass + other_mass.mass) * relative_velocity
            self.speed -= impulse / self.mass
            other_mass.speed += impulse / other_mass.mass

    def movement(self, masses: list):
        # Calculate the interaction between masses
        total_force = pygame.math.Vector2(0, 0)
        for mass in masses:
            if mass is not self:
                force = self.calculateGravitationalForce(mass)
                total_force += force

        # Handle collisions
        for mass in masses:
            if mass is not self:
                self.handle_collision(mass)

        # Modify the acceleration based on the total force
        self.acceleration = total_force / self.mass

        # Modify the position
        self.speed += self.acceleration
        self.position += self.speed

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update(self, screen: pygame.Surface, masses: list):
        self.movement(masses)
        self.draw(screen)

    def __repr__(self) -> str:
        return f'Mass: {self.mass} / Radius: {self.radius}'