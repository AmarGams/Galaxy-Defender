import pygame

from settings import *

from scale import scale

class EnemyBullet:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.speed = 10

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
            scale(6)
        )

    def off_screen(self):

        return self.y > HEIGHT