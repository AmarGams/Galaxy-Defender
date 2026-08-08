import pygame
from settings import *
from scale import scale

class Player:

    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80

    def draw(self, screen):

        pygame.draw.polygon(
            screen,
            BLUE,
            [
                (
                    self.x,
                    self.y - scale(30)
                ),
                (
                    self.x - scale(25),
                    self.y + scale(25)
                ),
                (
                    self.x + scale(25),
                    self.y + scale(25)
                )
            ]
        )

    def move(self, x, y):
        self.x = x
        self.y = y