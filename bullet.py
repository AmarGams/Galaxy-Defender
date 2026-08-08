import pygame
from settings import *
from scale import scale

class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 12

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(self.x),
                int(self.y)
            ),
            scale(5)
        )

    def off_screen(self):
        return self.y < 0