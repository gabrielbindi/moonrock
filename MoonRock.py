import pygame
import sys

pygame.init()
pygame.display.set_caption("MoonRock")

x = 400
y = 550
vel = 15

#setup for Pygame
screen = pygame.display.set_mode((800, 600))

player_img = pygame.image.load('Player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))


running = True

while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel

    if keys[pygame.K_RIGHT]:
        x += vel

    if keys[pygame.K_UP]:
        y -= vel

    if keys[pygame.K_DOWN]:
        y += vel

    #if keys[pygame.K_SPACE]:
    #add bullet class

    screen.fill((0, 0, 0))
    screen.blit(player_img, (x, y))
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit()
