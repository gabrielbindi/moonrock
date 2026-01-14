import random
import pygame
import sys
from pathlib import Path

"""Paths"""

BASE_DIR = Path(__file__).resolve().parent
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

SPAWN_EVENT = pygame.USEREVENT + 2
SPAWN_INTERVAL_MS = 900

"""Initial setup"""

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
alien_fast_img = pygame.image.load(str(ASSETS_DIR / "alien_fast.png")).convert_alpha()
alien_fast_img = pygame.transform.scale(alien_fast_img, (50, 50))

#SOUND
laser_sound = pygame.mixer.Sound(str(ASSETS_DIR / "laser_shot.wav"))
laser_sound.set_volume(0.4)

game_over_sound = pygame.mixer.Sound(str(ASSETS_DIR / "game_over.wav"))
game_over_sound.set_volume(0.6)

"""Sprites"""

class Player(pygame.sprite.Sprite):
    def __init__(self, image, start_pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=start_pos)
        self.last_shot_time = 0

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.speed_y = speed_y


    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
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

class AlienFast(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_fast_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.right >= WIDTH:
            self.direction = -1
            self.rect.y += 30
        elif self.rect.left <= 0:
            self.direction = 1
            self.rect.y += 30

def spawn_alien():
    x  = random.randint(50, WIDTH - 50)
    y = random.randint(40, 140)

    if random.random() < 0.7:
        return Alien(x, y)
    return AlienFast(x, y)



"""Groups"""

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player(player_img, (WIDTH // 2,  HEIGHT - 20))
all_sprites.add(player)

first_enemy = spawn_alien()
enemies.add(first_enemy)
all_sprites.add(first_enemy)

"""Player"""
player.rect.midbottom = (400, 550)
last_shot_time = 0

pygame.time.set_timer(TIMER_EVENT, TIMER_INTERVAL_MS)
pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL_MS)

"""Game Start"""
while running:
    dt = clock.tick(FPS)
    now = pygame.time.get_ticks()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == TIMER_EVENT:
            time_elapsed += 1

        if event.type == SPAWN_EVENT:
            enemy = spawn_alien()
            enemies.add(enemy)
            all_sprites.add(enemy)


    keys = pygame.key.get_pressed()
    player.update(keys)

    """Border"""
    player.rect.x = max(0, min(WIDTH - player.rect.width, player.rect.x))
    player.rect.y = max(0, min(HEIGHT - player.rect.height, player.rect.y))

    if keys[pygame.K_SPACE] and (now - last_shot_time) >= SHOT_COOLDOWN_MS:
        bullet = Bullet(bullet_img, player.rect.midtop, BULLET_SPEED)
        bullets.add(bullet)
        all_sprites.add(bullet)
        laser_sound.play()
        last_shot_time = now


    bullets.update()
    enemies.update()

    hit = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if hit:
        score += 1

    if pygame.sprite.spritecollideany(player, enemies):
        game_over_sound.play()
        running = False

    background_y += 1
    if background_y >= bg_h:
        background_y = 0


    screen.blit(background_image, (0, background_y))
    screen.blit(background_image, (0, background_y - bg_h))

    all_sprites.draw(screen)

    time_text = font.render(f"Time = {time_elapsed}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    score_text = font.render(f"Score = {score}", True, (255, 255, 255))
    screen.blit(score_text, (600, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()