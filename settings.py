# Screen

import pygame

pygame.init()

info = pygame.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 20)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)


import pygame

def scale_pos(x, y, screen_width, screen_height):
    scale_x = screen_width / WIDTH
    scale_y = screen_height / HEIGHT

    return (
        int(x * scale_x),
        int(y * scale_y)
    )