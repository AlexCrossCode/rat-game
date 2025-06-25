# menu.py

import pygame
from config import *

class Menu:
    def draw(self, surface):
        font = pygame.font.SysFont(None, 36)
        lines = [
            "Jogo em pausa [ESC]",
            "1: Equipar arma rápida",
            "2: Equipar arma pesada",
            "3: Equipar arco (placeholder)",
            "E: Spawnar inimigo",
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, GRAY)
            surface.blit(text, (100, 100 + i * 40))
