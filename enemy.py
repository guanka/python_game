import pygame
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

    def __init__(self):
        self.group = pygame.sprite.Group()

    def generate_enemy(self, env):
        y_axis = env.pos[0] - env.enemy1_rect.width
        enemy1_pos = [random.randint(0, y_axis), 0]
        enemy1 = Enemy(env.enemy1_img, env.enemy1_down_imgs, enemy1_pos)
        self.group.add(enemy1)