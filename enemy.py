import pygame
import random

import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed


class EnemyGroup:

    def __init__(self, env):
        self.enemy_group = pygame.sprite.Group()
        self.enemy_img = env.enemy1_img
        self.enemy_down_imgs = env.enemy1_down_imgs
        self.play_size = env.play_size
        self.env = env

    def generate(self):
        init_pos = [random.randint(0, self.play_size[0] - self.enemy_img.get_rect().width), 0]
        enemy_one = Enemy(self.enemy_img, self.enemy_down_imgs, init_pos)
        self.enemy_group.add(enemy_one)
        return self.enemy_group

    def enemy_down(self, index, down_rect):
        self.env.screen.blit(self.enemy_down_imgs[index], down_rect)


class PlayerVSEnemy:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.all_down_enemies = []

    def g_collide(self):
        self.all_down_enemies = pygame.sprite.groupcollide(self.enemies, self.player, True, True)




