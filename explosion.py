import pygame
from settings import *
from scale import scale

class Explosion:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 1

    def update(self):
        self.size += 1

    def finished(self):
        return self.size > 8

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(self.x),
                int(self.y)
            ),
            scale(self.size * 8),
            scale(2)
        )