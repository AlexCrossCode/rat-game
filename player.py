# player.py

import pygame
from config import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = WHITE
        self.speed = 4
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False
        self.weapon_type = "fast"
        self.health = 100
        self.attack_cooldown = 0

    def equip_weapon(self, weapon):
        self.weapon_type = weapon

    def update(self, keys, enemies):
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        dy += self.vel_y

        if self.rect.y + dy >= 500:
            dy = 500 - self.rect.y
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if keys[pygame.K_z] and self.attack_cooldown == 0:
            self.attack(enemies)
            self.attack_cooldown = 20

    def attack(self, enemies):
        attack_rect = self.rect.copy()
        attack_rect.width += 20
        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                enemy.health -= 10
                if enemy.health <= 0:
                    enemies.remove(enemy)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Weapon: {self.weapon_type}", True, YELLOW)
        surface.blit(text, (10, 10))
