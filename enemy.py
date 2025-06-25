# enemy.py

import pygame
from config import *

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = RED
        self.health = 30

    def update(self, player):
        pass  # podes adicionar lógica de movimento ou perseguição depois

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
