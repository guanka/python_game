import pygame
from sys import exit
from pygame.locals import *
import _random

# defination
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        else:
            self.rect.bottom += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        else:
            self.rect.right += self.speed


pygame.init()
# set screen size
screen = pygame.display.set_mode((800, 480))
# set background
background = pygame.image.load(r'ass.png').convert()
# set title
pygame.display.set_caption('air_plane')
# set image of player's plane

player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [600, 200]
plane_image = pygame.image.load(r'resources/image/shoot.png')

bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_image = plane_image.subsurface(bullet_rect)

player = Player(plane_image, player_rect, player_pos)
clock = pygame.time.Clock()

running = True

while running:
    # screen.fill(0)
    clock.tick(60)

    screen.fill(0)
    screen.blit(background, (0, 0))
    player.img_index += 1
    player.img_index %= 2
    screen.blit(player.image[player.img_index], player.rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w]:
        player.move_up()
    if key_pressed[K_s]:
        player.move_down()
    if key_pressed[K_a]:
        player.move_left()
    if key_pressed[K_d]:
        player.move_right()
    if key_pressed[K_SPACE]:
        player.shoot(bullet_image)
pygame.quit()
exit()
