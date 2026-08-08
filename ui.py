import pygame
from settings import *
from scale import scale

class UI:

    def __init__(self, font):
        self.font = font

    def draw(
        self,
        screen,
        score,
        high_score,
        lives,
        boss
    ):

        score_text = self.font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        high_score_text = self.font.render(
            f"High Score: {high_score}",
            True,
            YELLOW
        )

        lives_text = self.font.render(
            f"Lives: {lives}",
            True,
            GREEN
        )

        screen.blit(
            score_text,
            (scale(20), scale(20))
        )

        screen.blit(
            high_score_text,
            (scale(20), scale(60))
        )

        screen.blit(
            lives_text,
            (scale(20), scale(100))
        )

        if boss.active:

            pygame.draw.rect(
                screen,
                RED,
                (
                    WIDTH // 2 - scale(200),
                    scale(30),
                    scale(400),
                    scale(25)
                )
            )

            pygame.draw.rect(
                screen,
                GREEN,
                (
                    WIDTH // 2 - scale(200),
                    scale(30),
                    scale(400) * boss.hp / 20,
                    scale(25)
                )
            )

            text = self.font.render(
                "BOSS",
                True,
                WHITE
            )

            screen.blit(
                text,
                (
                    WIDTH // 2 - scale(35),
                    0
                )
            )