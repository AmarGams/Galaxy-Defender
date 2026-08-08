import pygame
import math
from settings import *
from scale import scale

class Boss:

    def __init__(self):
        self.active = False
        self.x = WIDTH // 2
        self.y = 120
        self.hp = 20
        self.speed = 8

    def spawn(self):
        self.active = True
        self.hp = 20
        self.x = WIDTH // 2

    def move(self):
        self.x += self.speed

        if self.x > WIDTH - 100 or self.x < 100:
            self.speed *= -1

    def hit(self):
        self.hp -= 1

        if self.hp <= 0:
            self.active = False
            return True

        return False

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (180, 0, 180),
            (int(self.x), int(self.y)),
            scale(60)
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x - 20), int(self.y - 15)),
            scale(8)
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x + 20), int(self.y - 15)),
            scale(8)
        )

        pygame.draw.arc(
            screen,
            RED,
            (self.x - 20, self.y, 40, 20),
            0,
            math.pi,
            scale(3)
        )