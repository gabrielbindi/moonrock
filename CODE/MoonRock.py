import pygame
import sys

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 48)
score = 0
time_left = 350

pygame.display.set_caption("MoonRock")

''' Variables '''

player_x = 400
player_y = 550
vel = 15

bullet_group = pygame.sprite.Group()

#setup for Pygame
screen = pygame.display.set_mode((800, 600))

''' Sprites '''

background = pygame.image.load('../Assets/background_Blue_Nebula_08.png').convert()

player_img = pygame.image.load('../Assets/Player.png').convert()
player_img = pygame.transform.scale(player_img, (50, 50))
bullet_img = pygame.image.load('../Assets/Laser Bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (8, 16))
bullet_img = pygame.transform.rotate(bullet_img, 180)

laser_sound = pygame.mixer.Sound('../Assets/laser_shot.wav')
laser_sound.set_volume(0.4)

game_over_sound = pygame.mixer.Sound('../Assets/game_over.wav')
game_over_sound.set_volume(0.6)

game_over_played = False

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

timer_event = pygame.USEREVENT +1 # 1s timer
pygame.time.set_timer(timer_event, 50)

running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer_event and time_left > 0:
            time_left -= 1 # faster or slower Countdown
        if time_left <= 0 and not game_over_played:
                game_over_sound.play()
                game_over_played = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x >= 0:
        player_x -= vel
    if keys[pygame.K_RIGHT] and player_x <= 750:
        player_x += vel
    if keys[pygame.K_UP] and player_y >= 0:
        player_y -= vel
    if keys[pygame.K_DOWN] and player_y <= 540:
        player_y += vel

    if keys[pygame.K_SPACE] and time_left > 0:
        bullet = Bullet(bullet_img, (player_x + 25, player_y + 30), -30) # "-10" laser firing speed
        bullet_group.add(bullet)
        score += 10
        laser_sound.play()


    '''Background'''
    screen.blit(background, (0, 0))
    '''Clock/Timer'''
    time_text = font.render(f"Time = {time_left}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))
    '''Score'''
    score_text = font.render(f"Score = {score}", True, (255, 255, 255))
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