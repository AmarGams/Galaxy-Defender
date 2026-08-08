import pygame
import random
from settings import *
from scale import scale

class Enemy:

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(-500, -50)
        self.speed = random.randint(2, 5)

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            RED,
            (
                int(self.x),
                int(self.y)
            ),
            scale(20)
        )