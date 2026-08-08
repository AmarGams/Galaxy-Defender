import pygame


class Display:

    def __init__(self):

        info = pygame.display.Info()

        self.screen_width = info.current_w
        self.screen_height = info.current_h

        self.base_width = 2560
        self.base_height = 1600

        self.scale_x = self.screen_width / self.base_width
        self.scale_y = self.screen_height / self.base_height

    def x(self, value):

        return int(value * self.scale_x)

    def y(self, value):

        return int(value * self.scale_y)

    def size(self, value):

        return int(
            value * min(
                self.scale_x,
                self.scale_y
            )
        )