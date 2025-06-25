# main.py

import pygame
from config import *
from player import Player
from enemy import Enemy
from weapon import Weapon
from menu import Menu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rat Game - Dev Mode")
clock = pygame.time.Clock()

player = Player(100, 500)
enemies = []
menu = Menu()

running = True
game_paused = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_paused = not game_paused

        if not game_paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.equip_weapon("fast")
                if event.key == pygame.K_2:
                    player.equip_weapon("heavy")
                if event.key == pygame.K_3:
                    player.equip_weapon("bow")
                if event.key == pygame.K_e:
                    enemies.append(Enemy(600, 500))

    if not game_paused:
        keys = pygame.key.get_pressed()
        player.update(keys, enemies)

        for enemy in enemies:
            enemy.update(player)

    screen.fill(BLACK)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    if game_paused:
        menu.draw(screen)

    pygame.display.flip()

pygame.quit()
