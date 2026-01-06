import pygame
import sys
from pathlib import Path

"""Paths"""

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "Assets"

"""Settings"""

WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_SPEED = 7
PLAYER_SIZE = (50, 50)

BULLET_SPEED = -12
SHOT_COOLDOWN_MS = 350

"""Timer"""

TIMER_EVENT = pygame.USEREVENT + 1
TIMER_INTERVAL_MS = 1000
time_elapsed = 0

"""Initial setup"""

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MoonRock")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 48)

score = 0
running = True

"""Assets"""

#BACKGROUND
background_image = pygame.image.load(str(ASSETS_DIR / "background_Blue_Nebula_08.png")).convert()
background_y = 0
bg_h = background_image.get_height()

#PLAYER
player_img = pygame.image.load(str(ASSETS_DIR / "Player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, PLAYER_SIZE)

#Bullet
bullet_img = pygame.image.load(str(ASSETS_DIR / "Laser Bullet.png")).convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (8, 16))
bullet_img = pygame.transform.rotate(bullet_img, 180)

#ALIEN
alien_img = pygame.image.load(str(ASSETS_DIR / "alien.png")).convert_alpha()
alien_img = pygame.transform.scale(alien_img, (50, 50))

#SOUND
laser_sound = pygame.mixer.Sound(str(ASSETS_DIR / "laser_shot.wav"))
laser_sound.set_volume(0.4)

game_over_sound = pygame.mixer.Sound(str(ASSETS_DIR / "game_over.wav"))
game_over_sound.set_volume(0.6)

"""Sprites"""

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:  # komplett aus dem Screen
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.right >= WIDTH:
            self.direction = -1
            self.rect.y += 20
        elif self.rect.left <= 0:
            self.direction = 1
            self.rect.y += 20


bullet_group = pygame.sprite.Group()
enemies = pygame.sprite.Group(Alien(100, 100))

"""Player"""
player_x, player_y = 400, 550
last_shot_time = 0


pygame.time.set_timer(TIMER_EVENT, TIMER_INTERVAL_MS)

"""Game Start"""
while running:
    dt = clock.tick(FPS)
    now = pygame.time.get_ticks()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == TIMER_EVENT:
            time_elapsed += 1


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_y += PLAYER_SPEED

    """Border"""
    player_x = max(0, min(WIDTH - PLAYER_SIZE[0], player_x))
    player_y = max(0, min(HEIGHT - PLAYER_SIZE[1], player_y))


    if keys[pygame.K_SPACE] and (now - last_shot_time) >= SHOT_COOLDOWN_MS:
        bullet = Bullet(
            bullet_img,
            (player_x + PLAYER_SIZE[0] // 2, player_y),
            BULLET_SPEED
        )
        bullet_group.add(bullet)
        laser_sound.play()
        last_shot_time = now


    bullet_group.update()
    enemies.update()


    background_y += 1
    if background_y >= bg_h:
        background_y = 0


    screen.blit(background_image, (0, background_y))
    screen.blit(background_image, (0, background_y - bg_h))

    enemies.draw(screen)
    bullet_group.draw(screen)

    screen.blit(player_img, (player_x, player_y))

    time_text = font.render(f"Time = {time_elapsed}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    score_text = font.render(f"Score = {score}", True, (255, 255, 255))
    screen.blit(score_text, (600, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
