import pygame
import random
from settings import *
from scale import scale

class Star:

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 4)

    def move(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.x = random.randint(0, WIDTH)
            self.y = 0

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(self.x),
                int(self.y)
            ),
            scale(self.speed)
        )