from settings import WIDTH, HEIGHT


BASE_WIDTH = 2560
BASE_HEIGHT = 1600


def scale(value):

    return int(
        value * min(
            WIDTH / BASE_WIDTH,
            HEIGHT / BASE_HEIGHT
        )
    )