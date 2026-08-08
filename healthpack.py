import pygame
import random

from settings import *

from scale import scale

class HealthPack:

    def __init__(self):

        self.reset()

    def reset(self):

        self.x = random.randint(50, WIDTH - 50)
        self.y = -50
        self.speed = 4
        self.active = False

    def spawn(self):

        self.active = True
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50

    def move(self):

        if self.active:

            self.y += self.speed

            if self.y > HEIGHT:

                self.reset()

    def draw(self, screen):

        if self.active:

            pygame.draw.circle(
                screen,
                GREEN,
                (
                    int(self.x),
                    int(self.y)
                ),
                scale(18)
            )

            pygame.draw.line(
                screen,
                WHITE,
                (
                    int(self.x - scale(8)),
                    int(self.y)
                ),
                (
                    int(self.x + scale(8)),
                    int(self.y)
                ),
                scale(3)
            )

            pygame.draw.line(
                screen,
                WHITE,
                (
                    int(self.x),
                    int(self.y - scale(8))
                ),
                (
                    int(self.x),
                    int(self.y + scale(8))
                ),
                scale(3)
            )