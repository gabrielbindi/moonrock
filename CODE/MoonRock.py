import pygame
import sys

pygame.init()
pygame.display.set_caption("MoonRock")

x = 400
y = 550
vel = 15
bvel= 30

#setup for Pygame
screen = pygame.display.set_mode((800, 600))

player_img = pygame.image.load('../Assets/Player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))
bullet_img = pygame.image.load('../Assets/Laser Bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (20, 20))
bullet_img = pygame.transform.rotate(bullet_img, 90)
running = True

#Bullet_Class:
#@param
#@return
class Projectile(object):
    def __init__(self, x, y, width, color, facing):
        self.x = x
        self.y = y
        self.width = width
        self.color = color
        self.facing = facing

while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x >= 0:
        x -= vel

    if keys[pygame.K_RIGHT] and x <= 750:
        x += vel

    if keys[pygame.K_UP] and y >= 0:
        y -= vel
    if keys[pygame.K_DOWN] and y <= 550:
        y += vel

    #if keys[pygame.K_SPACE]:
    #add bullet class

    screen.fill((0, 0, 0))
    screen.blit(player_img, (x, y))
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit()
