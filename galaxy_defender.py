import pygame
import random
import math

from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from boss import Boss
from explosion import Explosion
from star import Star
from healthpack import HealthPack
from ui import UI
from enemy_bullet import EnemyBullet
from powerup import PowerUp
from display import Display
print("1")
import camera
print("2")
HIGH_SCORE_FILE = "highscore.txt"
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

# =========================
# GAME SETTINGS
# =========================


# =========================
# SCREEN
# =========================
display_info = pygame.display.Info()

SCREEN_WIDTH = display_info.current_w

SCREEN_HEIGHT = display_info.current_h

screen = pygame.display.set_mode(
    (
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )
)

game_surface = pygame.Surface(
    (
        WIDTH,
        HEIGHT
    )
)

pygame.display.set_caption("Galaxy Defender")

display = Display()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
ui = UI(font)

# =========================
# PLAYER
# =========================
player = Player()

# =========================
# GAME VARIABLES
# =========================
score = 0
try:
    with open(HIGH_SCORE_FILE, "r") as file:
        high_score = int(file.read())
except:
    high_score = 0
lives = 3
dragging = False
shoot_timer = 0
rapid_fire = False
rapid_fire_timer = 0

# =========================
# OBJECTS
# =========================
bullets = []
stars = [Star() for i in range(120)]
enemies = [Enemy() for i in range(5)]
explosions = []
enemy_bullets = []

# Boss
boss = Boss()
BOSS_MAX_HP = 20

health_pack = HealthPack()

power_up = PowerUp()

# =========================
# CREATE STARS
# =========================


# =========================
# CREATE ENEMIES
# =========================

# =========================
# GAME LOOP
# =========================
running = True
game_over = False
show_title = True

while running:

    clock.tick(FPS)

    # ---------------------
    # EVENTS
    # ---------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if show_title:

                show_title = False

                continue

            if game_over:

                score = 0

                lives = 3

                bullets.clear()

                enemy_bullets.clear()

                explosions.clear()

                enemies = [Enemy() for i in range(5)]

                boss = Boss()

                health_pack = HealthPack()

                power_up = PowerUp()

                rapid_fire = False

                rapid_fire_timer = 0

                game_over = False

                continue
            dragging = True

            player.move(
                event.pos[0] * WIDTH / SCREEN_WIDTH,
                event.pos[1] * HEIGHT / SCREEN_HEIGHT
            )


        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:

            player.move(
                event.pos[0] * WIDTH / SCREEN_WIDTH,
                event.pos[1] * HEIGHT / SCREEN_HEIGHT
            )

    if not game_over and not show_title:

        # -----------------
        # SHOOT
        # -----------------
        shoot_timer += 1

        if shoot_timer >= (4 if rapid_fire else 12):
            bullets.append(Bullet(player.x, player.y - 25))
            shoot_timer = 0
      

        # -----------------
        # MOVE BULLETS
        # -----------------
        for bullet in bullets[:]:
            bullet.move()

            if bullet.off_screen():
                bullets.remove(bullet)
                
        for bullet in enemy_bullets[:]:

            bullet.move()

            if bullet.off_screen():

                enemy_bullets.remove(bullet)

        # -----------------
        # MOVE STARS
        # -----------------
        for star in stars:
              star.move()

        # -----------------
        # MOVE ENEMIES
        # -----------------
        for enemy in enemies:

            enemy.move()
            
            if random.randint(1, 120) == 1:

                enemy_bullets.append(
                    EnemyBullet(
                        enemy.x,
                        enemy.y
                    )
                )

            if enemy.y > HEIGHT + 30:

                enemy.reset()

                lives -= 1

            # Bullet Collision
            for bullet in bullets[:]:

                if math.hypot(
                    bullet.x - enemy.x,
                    bullet.y - enemy.y
                ) < 25:

                    bullets.remove(bullet)

                    score += 1

                    if score > high_score:

                        high_score = score

                        with open(HIGH_SCORE_FILE, "w") as file:

                            file.write(str(high_score))

                    explosions.append(
                        Explosion(enemy.x, enemy.y)
                    )

                    enemy.reset()

                    break
        # Boss collision
        if boss.active:

            for bullet in bullets[:]:

                if math.hypot(
                    bullet.x - boss.x,
                    bullet.y - boss.y
                ) < 60:

                    bullets.remove(bullet)

                    explosions.append(
                           Explosion(boss.x, boss.y)
                    )

                    if boss.hit():

                        score += 50

                        if score > high_score:

                            high_score = score

                            with open(HIGH_SCORE_FILE, "w") as file:

                                file.write(str(high_score))

        if health_pack.active:

            if math.hypot(
                player.x - health_pack.x,
                player.y - health_pack.y
            ) < 35:

                lives += 1

                health_pack.reset()

                explosions.append(
                    Explosion(
                        health_pack.x,
                        health_pack.y
                    )
                )

        if lives <= 0:
            game_over = True
        if score >= 10 and not boss.active:
           boss.spawn()
        if boss.active:
             boss.move()

        if rapid_fire:

            rapid_fire_timer -= 1

            if rapid_fire_timer <= 0:

                rapid_fire = False
           
        if random.randint(1, 30) == 1:

            if not health_pack.active:

                health_pack.spawn()

        health_pack.move()
        
        if random.randint(1, 200) == 1:

            if not power_up.active:

                power_up.spawn()

        power_up.move()
        
        if power_up.active:

            if math.hypot(
                player.x - power_up.x,
                player.y - power_up.y
            ) < 35:

                power_up.active = False

                rapid_fire = True

                rapid_fire_timer = FPS * 8

                score += 10

                if score > high_score:

                    high_score = score

                    with open(HIGH_SCORE_FILE, "w") as file:

                        file.write(str(high_score))

    # =====================
    # DRAW
    # =====================
    screen.fill(BLACK)
    
    if show_title:

        title = font.render(
            "GALAXY DEFENDER",
            True,
            WHITE
        )

        version = font.render(
            "Version 1.0",
            True,
            GREEN
        )

        start = font.render(
            "Tap Anywhere To Start",
            True,
            YELLOW
        )

        screen.blit(
            title,
            (WIDTH // 2 - 220, HEIGHT // 2 - 100)
        )

        screen.blit(
            version,
            (WIDTH // 2 - 70, HEIGHT // 2 - 20)
        )

        screen.blit(
            start,
            (WIDTH // 2 - 180, HEIGHT // 2 + 60)
        )

        pygame.display.update()

        continue

    # Stars
    for star in stars:
          star.draw(screen)

    if show_title:

        screen.fill(BLACK)

        title = font.render(
            "GALAXY DEFENDER",
            True,
            WHITE
        )

        version = font.render(
            "Version 1.0",
            True,
            GREEN
        )

        start = font.render(
            "Tap Anywhere To Start",
            True,
            YELLOW
        )

        screen.blit(
            title,
            (WIDTH//2 - 180, HEIGHT//2 - 80)
        )

        screen.blit(
            version,
            (WIDTH//2 - 70, HEIGHT//2)
        )

        screen.blit(
            start,
            (WIDTH//2 - 170, HEIGHT//2 + 80)
        )


        continue
        
    if not game_over:

        # Ship
        player.draw(screen)

        # Bullets
        for bullet in bullets:
              bullet.draw(screen)
              
        for bullet in enemy_bullets:

            bullet.draw(screen)

        # Enemies
        for enemy in enemies:
              enemy.draw(screen)
        if boss.active:
            boss.draw(screen)
            
        health_pack.draw(screen)
        
        power_up.draw(screen)
      
    else:

        text = font.render(
            "GAME OVER",
            True,
            RED
        )

        restart = font.render(
            "Tap Anywhere To Restart",
            True,
            WHITE
        )

        screen.blit(
            text,
            (WIDTH // 2 - 120, HEIGHT // 2 - 40)
        )

        screen.blit(
            restart,
            (WIDTH // 2 - 180, HEIGHT // 2 + 30)
        )

    # UI
    ui.draw(
        screen,
        score,
        high_score,
        lives,
        boss
    )

    for explosion in explosions[:]:

        explosion.update()

        explosion.draw(screen)

        if explosion.finished():
            explosions.remove(explosion)

    pygame.display.update()

pygame.display.update()

pygame.quit()