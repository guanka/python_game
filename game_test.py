import pygame
from sys import exit
from pygame.locals import *
import random
from player import *
from enemy import *

# defination
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800




pygame.init()
# set screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set background
background = pygame.image.load(r'resources/image/background.png').convert()
# set title
pygame.display.set_caption('air_plane')
# set image of player's plane
plane_image = pygame.image.load(r'resources/image/shoot.png')
# init player
play_size = [SCREEN_WIDTH, SCREEN_HEIGHT]
player = init_player(plane_image, play_size)
# init bullet
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_image = plane_image.subsurface(bullet_rect)

# enemy img
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_image.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_image.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_image.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_image.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_image.subsurface(pygame.Rect(930, 697, 57, 43)))
enemies1 = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()

# parameter init
enemy_frequency = 0
clock = pygame.time.Clock()
bullet_time = 0
score = 0
player_img_control = 0
player_down_index = 4
running = True

while running:
    # screen.fill(0)
    clock.tick(60)
    # screen clear
    screen.fill(0)
    # draw the background
    screen.blit(background, (0, 0))
    # generate the enemy-plane
    
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0
    # enemy move and enemy collide with player
    for enemy in enemies1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
        if enemy.rect.top < 0:
            enemies1.remove(enemy)
    # enemy collide with bullets
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    # enemy crash
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        a = int(enemy_down.down_index / 2)

        screen.blit(enemy1_down_imgs[int(enemy_down.down_index / 2)], enemy_down.rect)
        enemy_down.down_index += 1
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
    else:
        player.img_index = int(player_down_index / 2)
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        print(player_down_index)
        print(player.img_index)
        if player_down_index > 11:
            running = False
    player.bullets.draw(screen)
    enemies1.draw(screen)

    bullet_time += 1
    player_img_control += 1
    if player_img_control > 6:
        player_img_control = 0
        player.img_index = 1 - player.img_index
    screen.blit(player.image[player.img_index], player.rect)
    # show the score
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)
    pygame.display.update()
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)
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
        if bullet_time > 8:
            bullet_time = 0
            player.shoot(bullet_image)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            exit()
        pygame.display.update()