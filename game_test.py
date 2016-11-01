import pygame
from sys import exit
from pygame.locals import *
import random
from player import *
from enemy import *

# defination
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800


class Env:

    def __init__(self):
        self.__game_init()
        self.background = pygame.image.load(r'resources/image/background.png').convert()
        self.plane_image = pygame.image.load(r'resources/image/shoot.png')
        self.__bullet_init()
        self.__enemy_init()
        self.__parameter_init()
        self.player = init_player(self.plane_image, self.play_size)

    def __game_init(self):
        pygame.init()
        self.play_size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode((self.play_size[0], self.play_size[1]))
        self.clock = pygame.time.Clock()

    def __bullet_init(self):
        self.bullet_rect = pygame.Rect(1004, 987, 9, 21)
        self.bullet_image = self.plane_image.subsurface(self.bullet_rect)

    def __enemy_init(self):
        self.enemy1_rect = pygame.Rect(534, 612, 57, 43)
        self.enemy1_img = self.plane_image.subsurface(self.enemy1_rect)
        self.enemy1_down_imgs = []
        self.enemy1_down_imgs.append(self.plane_image.subsurface(pygame.Rect(267, 347, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_image.subsurface(pygame.Rect(873, 697, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_image.subsurface(pygame.Rect(267, 296, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_image.subsurface(pygame.Rect(930, 697, 57, 43)))
        self.enemies1 = pygame.sprite.Group()
        self.enemies_down = pygame.sprite.Group()

    def __parameter_init(self):
        self.enemy_frequency = 0
        self.bullet_time = 0
        self.score = 0
        self.player_img_control = 0
        self.player_down_index = 4
        self.running = True

    def game_bg_render(self):
        # screen.fill(0)
        self.clock.tick(60)
        # screen clear
        self.screen.fill(0)
        # draw the background
        self.screen.blit(env.background, (0, 0))
        # generate the enemy-plane

# project init
env = Env()

while env.running:
    env.game_bg_render()
    
    if env.enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - env.enemy1_rect.width), 0]
        enemy1 = Enemy(env.enemy1_img, env.enemy1_down_imgs, enemy1_pos)
        env.enemies1.add(enemy1)
    env.enemy_frequency += 1
    if env.enemy_frequency >= 100:
        env.enemy_frequency = 0
    # enemy move and enemy collide with player
    for enemy in env.enemies1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, env.player):
            env.enemies_down.add(enemy)
            env.enemies1.remove(enemy)
            env.player.is_hit = True
        if enemy.rect.top < 0:
            env.enemies1.remove(enemy)
    # enemy collide with bullets
    enemies1_down = pygame.sprite.groupcollide(env.enemies1, env.player.bullets, 1, 1)
    # enemy crash
    for enemy_down in enemies1_down:
        env.enemies_down.add(enemy_down)

    for enemy_down in env.enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            env.enemies_down.remove(enemy_down)
            env.score += 1000
            continue
        a = int(enemy_down.down_index / 2)

        env.screen.blit(env.enemy1_down_imgs[int(enemy_down.down_index / 2)], enemy_down.rect)
        enemy_down.down_index += 1

    if not env.player.is_hit:
        env.screen.blit(env.player.image[env.player.img_index], env.player.rect)
    else:
        env.player.img_index = int(env.player_down_index / 2)
        env.screen.blit(env.player.image[env.player.img_index], env.player.rect)
        env.player_down_index += 1
        print(env.player_down_index)
        print(env.player.img_index)
        if env.player_down_index > 11:
            env.running = False
    env.player.bullets.draw(env.screen)
    env.enemies1.draw(env.screen)

    env.bullet_time += 1
    env.player_img_control += 1
    if env.player_img_control > 6:
        env.player_img_control = 0
        env.player.img_index = 1 - env.player.img_index
    env.screen.blit(env.player.image[env.player.img_index], env.player.rect)
    # show the score
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(env.score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    env.screen.blit(score_text, text_rect)
    pygame.display.update()
    for bullet in env.player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            env.player.bullets.remove(bullet)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w]:
        env.player.move_up()
    if key_pressed[K_s]:
        env.player.move_down()
    if key_pressed[K_a]:
        env.player.move_left()
    if key_pressed[K_d]:
        env.player.move_right()
    if key_pressed[K_SPACE]:
        if env.bullet_time > 8:
            env.bullet_time = 0
            env.player.shoot(env.bullet_image)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            exit()
        pygame.display.update()