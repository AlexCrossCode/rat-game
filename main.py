# main.py

import pygame
from config import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rat Game")
clock = pygame.time.Clock()

# Criar jogador
player = Player(100, 400)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Desenhar
    screen.fill(BLACK)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
