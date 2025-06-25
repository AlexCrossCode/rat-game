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

    def update(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        # Saltar
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        dy += self.vel_y

        # Simples deteção de chão
        if self.rect.y + dy >= 500:
            dy = 500 - self.rect.y
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
