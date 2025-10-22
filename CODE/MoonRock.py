import pygame
import sys

pygame.init()
pygame.display.set_caption("MoonRock")

''' Variables '''

player_x = 400
player_y = 550
vel = 15

last_shot = 0
shot_cooldown = 400

bullet_group = pygame.sprite.Group()


#setup for Pygame
screen = pygame.display.set_mode((800, 600))

''' Sprites '''

background = pygame.image.load('../moonrock/Assets/background_Blue_Nebula_08.png').convert()
player_img = pygame.image.load('../moonrock/Assets/Player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))
bullet_img = pygame.image.load('../moonrock/Assets/Laser Bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (8, 16))
bullet_img = pygame.transform.rotate(bullet_img, 180)


font = pygame.font.Font(None, 48)
score = 0
time_left = 350


running = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = start_pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.kill()

while running:
    pygame.time.delay(100)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_LEFT] and player_x >= 0:
        player_x -= vel
    if keys[pygame.K_RIGHT] and player_x <= 750:
        player_x += vel
    if keys[pygame.K_UP] and player_y >= 0:
        player_y -= vel
    if keys[pygame.K_DOWN] and player_y <= 540:
        player_y += vel

    if keys[pygame.K_SPACE] and current_time - last_shot > shot_cooldown:
        bullet = Bullet(bullet_img, (player_x + 25, player_y + 30), -10)
        bullet_group.add(bullet)
        last_shot = current_time

    screen.fill((0, 0, 0))

    '''Background'''
    screen.blit(background, (0, 0))
    '''Clock/Timer'''
    time_text = font.render("Time = 350", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))
    '''Score'''
    score_text = font.render("Score = 0", True, (255, 255, 255))
    screen.blit(score_text, (600, 10))
    '''Player'''
    screen.blit(player_img, (player_x, player_y))
    '''Bullet'''
    bullet_group.update()
    bullet_group.draw(screen)
    '''Display'''
    pygame.display.update()
    pygame.display.flip()




pygame.quit()
sys.exit()
