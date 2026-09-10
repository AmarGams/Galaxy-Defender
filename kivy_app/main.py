"""Galaxy Defender - Kivy Android edition."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.uix.widget import Widget


FPS = 60

WHITE = (1, 1, 1, 1)
BLUE = (0.2, 0.6, 1, 1)
RED = (1, 0.2, 0.2, 1)
GREEN = (0.2, 1, 0.3, 1)
YELLOW = (1, 0.9, 0.1, 1)
PURPLE = (0.7, 0.1, 0.8, 1)
BACKGROUND = (0, 0, 0.08, 1)


@dataclass
class Sprite:
    x: float
    y: float
    speed: float = 0


class GalaxyDefender(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.state = "title"

        self.score = 0
        self.lives = 3
        self.cooldown = 0
        self.rapid_for = 0

        self.boss = None
        self.boss_hp = 20

        self.health = None
        self.power = None

        self.bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.enemies = []
        self.stars = []

        self.music = None

        self.score_file = None
        self.high_score = 0

        self.bind(
            size=self.on_size,
            pos=self.on_size
        )

        self.setup_high_score()
        self.reset()

        Clock.schedule_once(
            self.finish_setup,
            0
        )

        Clock.schedule_interval(
            self.update,
            1 / FPS
        )

    # ---------------------------------------------------------
    # SETUP
    # ---------------------------------------------------------

    def finish_setup(self, *_):
        self.create_stars()
        self.reset()
        self.load_music()
        self._draw()

    def setup_high_score(self):
        app = App.get_running_app()

        self.score_file = (
            Path(app.user_data_dir)
            / "highscore.txt"
        )

        try:
            self.high_score = int(
                self.score_file.read_text(
                    encoding="utf-8"
                ).strip()
            )
        except (OSError, ValueError):
            self.high_score = 0

    def load_music(self):
        music_path = (
            Path(__file__).resolve().parent
            / "music.mp3"
        )

        if not music_path.exists():
            return

        try:
            self.music = SoundLoader.load(
                str(music_path)
            )

            if self.music is not None:
                self.music.loop = True
                self.music.volume = 0.7
                self.music.play()

        except Exception:
            self.music = None

    # ---------------------------------------------------------
    # SCREEN / RESOLUTION
    # ---------------------------------------------------------

    def on_size(self, *_):
        if self.width <= 0 or self.height <= 0:
            return

        if hasattr(self, "player"):
            self.player.x = min(
                max(self.player.x, 25),
                max(25, self.width - 25)
            )

            self.player.y = min(
                max(self.player.y, 35),
                max(35, self.height - 35)
            )

        self._draw()

    # ---------------------------------------------------------
    # GAME RESET
    # ---------------------------------------------------------

    def reset(self):
        self.score = 0
        self.lives = 3

        self.cooldown = 0
        self.rapid_for = 0

        self.boss = None
        self.boss_hp = 20

        self.health = None
        self.power = None

        self.bullets.clear()
        self.enemy_bullets.clear()
        self.explosions.clear()

        self.player = Sprite(
            self.width / 2,
            max(60, self.height - 100)
        )

        self.create_stars()

        self.enemies = [
            self.new_enemy()
            for _ in range(5)
        ]

    def create_stars(self):
        if self.width <= 0 or self.height <= 0:
            return

        self.stars = [
            Sprite(
                random.uniform(
                    0,
                    self.width
                ),
                random.uniform(
                    0,
                    self.height
                ),
                random.uniform(
                    40,
                    180
                )
            )
            for _ in range(100)
        ]

    # ---------------------------------------------------------
    # ENEMIES
    # ---------------------------------------------------------

    def new_enemy(self):
        return Sprite(
            random.uniform(
                35,
                max(
                    36,
                    self.width - 35
                )
            ),
            random.uniform(
                -500,
                -40
            ),
            random.uniform(
                90,
                220
            )
        )

    def reset_enemy(
        self,
        enemy,
        lost_life=False
    ):
        fresh = self.new_enemy()

        enemy.x = fresh.x
        enemy.y = fresh.y
        enemy.speed = fresh.speed

        if lost_life:
            self.lives -= 1

    # ---------------------------------------------------------
    # COLLISION
    # ---------------------------------------------------------

    @staticmethod
    def near(a, b, distance):
        return (
            math.hypot(
                a.x - b.x,
                a.y - b.y
            )
            < distance
        )

    # ---------------------------------------------------------
    # SCORE
    # ---------------------------------------------------------

    def add_score(self, amount):
        self.score += amount

        if self.score > self.high_score:
            self.high_score = self.score

            try:
                self.score_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                self.score_file.write_text(
                    str(self.high_score),
                    encoding="utf-8"
                )

            except OSError:
                pass

    # ---------------------------------------------------------
    # TOUCH CONTROLS
    # ---------------------------------------------------------

    def on_touch_down(self, touch):

        if self.state == "title":
            self.reset()
            self.state = "playing"

        elif self.state == "game_over":
            self.reset()
            self.state = "playing"

        self.move_player(
            touch.x,
            touch.y
        )

        return True

    def on_touch_move(self, touch):

        if self.state == "playing":
            self.move_player(
                touch.x,
                touch.y
            )

        return True

    def move_player(self, x, y):

        if self.width <= 0 or self.height <= 0:
            return

        self.player.x = min(
            max(x, 25),
            max(25, self.width - 25)
        )

        self.player.y = min(
            max(y, 35),
            max(35, self.height - 35)
        )

    # ---------------------------------------------------------
    # MAIN UPDATE
    # ---------------------------------------------------------

    def update(self, dt):

        dt = min(
            max(dt, 0),
            0.05
        )

        if self.state == "playing":
            self.advance(dt)

        self._draw()

    # ---------------------------------------------------------
    # GAME LOGIC
    # ---------------------------------------------------------

    def advance(self, dt):

        self.cooldown -= dt

        self.rapid_for = max(
            0,
            self.rapid_for - dt
        )

        # Automatic player shooting
        if self.cooldown <= 0:

            self.bullets.append(
                Sprite(
                    self.player.x,
                    self.player.y + 30,
                    720
                )
            )

            self.cooldown = (
                0.07
                if self.rapid_for > 0
                else 0.20
            )

        # Stars
        for star in self.stars:

            star.y -= (
                star.speed * dt
            )

            if star.y < 0:

                star.x = random.uniform(
                    0,
                    self.width
                )

                star.y = self.height

        self.move_bullets(dt)
        self.move_enemies(dt)
        self.move_boss(dt)
        self.move_pickups(dt)
        self.update_explosions(dt)

        if self.lives <= 0:
            self.lives = 0
            self.state = "game_over"

    # ---------------------------------------------------------
    # BULLETS
    # ---------------------------------------------------------

    def move_bullets(self, dt):

        for bullet in self.bullets[:]:

            bullet.y += (
                bullet.speed * dt
            )

            if bullet.y > self.height + 20:

                if bullet in self.bullets:
                    self.bullets.remove(
                        bullet
                    )

        for bullet in self.enemy_bullets[:]:

            bullet.y -= (
                bullet.speed * dt
            )

            if bullet.y < -20:

                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(
                        bullet
                    )

                continue

            if self.near(
                bullet,
                self.player,
                25
            ):

                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(
                        bullet
                    )

                self.damage_player()

    # ---------------------------------------------------------
    # ENEMIES
    # ---------------------------------------------------------

    def move_enemies(self, dt):

        for enemy in self.enemies:

            enemy.y -= (
                enemy.speed * dt
            )

            # Enemy shooting
            if random.random() < dt * 0.5:

                self.enemy_bullets.append(
                    Sprite(
                        enemy.x,
                        enemy.y - 20,
                        360
                    )
                )

            # Enemy reaches bottom
            if enemy.y < -35:

                self.reset_enemy(
                    enemy,
                    True
                )

                continue

            # Player bullets hitting enemy
            destroyed = False

            for bullet in self.bullets[:]:

                if self.near(
                    bullet,
                    enemy,
                    25
                ):

                    if bullet in self.bullets:
                        self.bullets.remove(
                            bullet
                        )

                    self.explode(
                        enemy.x,
                        enemy.y
                    )

                    self.add_score(1)

                    self.reset_enemy(
                        enemy
                    )

                    destroyed = True
                    break

            if destroyed:
                continue

            # Enemy hitting player
            if self.near(
                enemy,
                self.player,
                35
            ):

                self.reset_enemy(
                    enemy
                )

                self.damage_player()

    # ---------------------------------------------------------
    # PLAYER DAMAGE
    # ---------------------------------------------------------

    def damage_player(self):

        self.lives -= 1

        self.explode(
            self.player.x,
            self.player.y
        )

    # ---------------------------------------------------------
    # EXPLOSIONS
    # ---------------------------------------------------------

    def explode(self, x, y):

        self.explosions.append(
            [x, y, 0]
        )

    def update_explosions(self, dt):

        updated = []

        for x, y, age in self.explosions:

            age += dt

            if age < 0.35:
                updated.append(
                    [x, y, age]
                )

        self.explosions = updated

    # ---------------------------------------------------------
    # BOSS
    # ---------------------------------------------------------

    def spawn_boss(self):

        self.boss = Sprite(
            self.width / 2,
            self.height - 140,
            200
        )

        self.boss_hp = 20

    def move_boss(self, dt):

        if (
            self.score >= 10
            and self.boss is None
        ):
            self.spawn_boss()

        if self.boss is None:
            return

        self.boss.x += (
            self.boss.speed * dt
        )

        if (
            self.boss.x >= self.width - 70
            or self.boss.x <= 70
        ):

            self.boss.speed *= -1

            self.boss.x = min(
                max(
                    self.boss.x,
                    70
                ),
                max(
                    70,
                    self.width - 70
                )
            )

        # Boss shooting
        if random.random() < dt * 0.8:

            self.enemy_bullets.append(
                Sprite(
                    self.boss.x,
                    self.boss.y - 65,
                    420
                )
            )

        # Player bullets hitting boss
        for bullet in self.bullets[:]:

            if self.near(
                bullet,
                self.boss,
                65
            ):

                if bullet in self.bullets:
                    self.bullets.remove(
                        bullet
                    )

                self.boss_hp -= 1

                self.explode(
                    self.boss.x,
                    self.boss.y
                )

                if self.boss_hp <= 0:

                    self.explode(
                        self.boss.x,
                        self.boss.y
                    )

                    self.add_score(50)

                    self.boss = None
                    self.boss_hp = 20

                break

        # Boss touching player
        if (
            self.boss is not None
            and self.near(
                self.boss,
                self.player,
                80
            )
        ):

            self.damage_player()

    # ---------------------------------------------------------
    # POWER-UPS
    # ---------------------------------------------------------

    def move_pickups(self, dt):

        # Health pickup
        if (
            self.health is None
            and random.random() < dt / 4
        ):

            self.health = Sprite(
                random.uniform(
                    35,
                    max(
                        36,
                        self.width - 35
                    )
                ),
                self.height + 30,
                130
            )

        # Rapid fire pickup
        if (
            self.power is None
            and random.random() < dt / 12
        ):

            self.power = Sprite(
                random.uniform(
                    35,
                    max(
                        36,
                        self.width - 35
                    )
                ),
                self.height + 30,
                150
            )

        for name in (
            "health",
            "power"
        ):

            pickup = getattr(
                self,
                name
            )

            if pickup is None:
                continue

            pickup.y -= (
                pickup.speed * dt
            )

            if pickup.y < -30:

                setattr(
                    self,
                    name,
                    None
                )

                continue

            if self.near(
                pickup,
                self.player,
                35
            ):

                if name == "health":

                    self.lives = min(
                        self.lives + 1,
                        5
                    )

                else:

                    self.rapid_for = 8

                    self.add_score(10)

                self.explode(
                    pickup.x,
                    pickup.y
                )

                setattr(
                    self,
                    name,
                    None
                )

    # ---------------------------------------------------------
    # DRAWING
    # ---------------------------------------------------------

    def _draw(self):

        self.canvas.clear()

        if self.width <= 0 or self.height <= 0:
            return

        with self.canvas:

            # Background
            Color(*BACKGROUND)

            Rectangle(
                pos=self.pos,
                size=self.size
            )

            # Stars
            Color(*WHITE)

            for star in self.stars:

                Ellipse(
                    pos=(
                        star.x - 2,
                        star.y - 2
                    ),
                    size=(4, 4)
                )

            if self.state == "title":

                self.draw_title()

            elif self.state == "game_over":

                self.draw_game_over()

            else:

                self.draw_scene()

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    def draw_title(self):

        self.label(
            "GALAXY DEFENDER",
            self.height / 2 + 40,
            42,
            BLUE
        )

        self.label(
            "Version 1.0",
            self.height / 2 - 15,
            22,
            GREEN
        )

        self.label(
            "Tap anywhere to start",
            self.height / 2 - 70,
            25,
            YELLOW
        )

    # ---------------------------------------------------------
    # GAME OVER
    # ---------------------------------------------------------

    def draw_game_over(self):

        self.label(
            "GAME OVER",
            self.height / 2 + 30,
            42,
            RED
        )

        self.label(
            (
                f"Score: {self.score}"
                f"   Best: {self.high_score}"
            ),
            self.height / 2 - 25,
            22,
            WHITE
        )

        self.label(
            "Tap anywhere to restart",
            self.height / 2 - 80,
            24,
            YELLOW
        )

    # ---------------------------------------------------------
    # GAME SCENE
    # ---------------------------------------------------------

    def draw_scene(self):

        # Player
        Color(*BLUE)

        Triangle(
            points=[
                self.player.x,
                self.player.y + 30,

                self.player.x - 25,
                self.player.y - 25,

                self.player.x + 25,
                self.player.y - 25
            ]
        )

        # Player bullets
        Color(*YELLOW)

        for bullet in self.bullets:

            Ellipse(
                pos=(
                    bullet.x - 5,
                    bullet.y - 5
                ),
                size=(10, 10)
            )

        # Enemy bullets
        Color(*RED)

        for bullet in self.enemy_bullets:

            Ellipse(
                pos=(
                    bullet.x - 6,
                    bullet.y - 6
                ),
                size=(12, 12)
            )

        # Enemies
        Color(*RED)

        for enemy in self.enemies:

            Ellipse(
                pos=(
                    enemy.x - 18,
                    enemy.y - 18
                ),
                size=(36, 36)
            )

        # Boss
        if self.boss is not None:

            Color(*PURPLE)

            Ellipse(
                pos=(
                    self.boss.x - 60,
                    self.boss.y - 60
                ),
                size=(120, 120)
            )

            Color(*RED)

            bar_w = max(
                0,
                120 * (
                    self.boss_hp / 20
                )
            )

            Rectangle(
                pos=(
                    self.boss.x - 60,
                    self.boss.y + 70
                ),
                size=(bar_w, 8)
            )

        # Health pack
        if self.health is not None:

            Color(*GREEN)

            Ellipse(
                pos=(
                    self.health.x - 14,
                    self.health.y - 14
                ),
                size=(28, 28)
            )

        # Rapid-fire pack
        if self.power is not None:

            Color(*YELLOW)

            Ellipse(
                pos=(
                    self.power.x - 14,
                    self.power.y - 14
                ),
                size=(28, 28)
            )

        # Explosions
        for x, y, age in self.explosions:

            Color(
                1,
                0.6,
                0.1,
                max(0, 1 - age / 0.35)
            )

            r = 10 + age * 80

            Ellipse(
                pos=(
                    x - r / 2,
                    y - r / 2
                ),
                size=(r, r)
            )

        # HUD
        self.label(
            f"Score {self.score}",
            self.height - 40,
            22,
            WHITE,
            20
        )

        self.label(
            f"Best {self.high_score}",
            self.height - 70,
            18,
            YELLOW,
            20
        )

        lives_text = f"Lives {self.lives}"

        self.label(
            lives_text,
            self.height - 40,
            22,
            GREEN,
            max(
                20,
                self.width - 160
            )
        )

        if self.rapid_for > 0:

            self.label(
                "RAPID",
                self.height - 70,
                18,
                BLUE,
                max(
                    20,
                    self.width - 160
                )
            )

    # ---------------------------------------------------------
    # TEXT
    # ---------------------------------------------------------

    def label(
        self,
        text,
        y,
        font_size,
        color,
        x=None
    ):

        lbl = CoreLabel(
            text=str(text),
            font_size=font_size
        )

        lbl.refresh()

        tex = lbl.texture

        if tex is None:
            return

        if x is None:

            x = (
                self.width / 2
                - tex.width / 2
            )

        Color(*color)

        Rectangle(
            texture=tex,
            pos=(x, y),
            size=tex.size
        )


class GalaxyDefenderApp(App):

    def build(self):

        self.title = "Galaxy Defender"

        return GalaxyDefender()


if __name__ == "__main__":

    GalaxyDefenderApp().run()
