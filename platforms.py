import pygame
from config import *

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY

    def draw(self, surface, camera_x=0, camera_y=0):
        offset_rect = self.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(surface, self.color, offset_rect)
