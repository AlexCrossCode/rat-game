import pygame
from config import *
from player import Player
from enemy import Enemy
from menu import Menu
from map import load_map
from platforms import Platform

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rat Game - Dev Mode")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

player = Player(100, 200)
enemies = []
menu = Menu()

# Carregar mapa
current_room = 1
level_map = load_map(current_room)

tile_size = 40
platforms = []

# Passo 1: Criar plataformas
for row_index, row in enumerate(level_map):
    for col_index, cell in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        if cell == "#":
            platforms.append(Platform(x, y, tile_size, 20))

# Passo 2: Criar inimigos
for row_index, row in enumerate(level_map):
    for col_index, cell in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        if cell == "E":
            enemies.append(Enemy(x, y))

running = True
paused = False

while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            if paused:
                if event.key == pygame.K_r:
                    player = Player(100, 200)
                    enemies = []
                if event.key == pygame.K_e:
                    enemies.append(Enemy(player.rect.x + 100, player.rect.y))
                if event.key == pygame.K_q:
                    player.current_weapon_index = (player.current_weapon_index - 1) % len(player.inventory)
                    player.current_weapon = player.inventory[player.current_weapon_index]
                if event.key == pygame.K_w:
                    player.current_weapon_index = (player.current_weapon_index + 1) % len(player.inventory)
                    player.current_weapon = player.inventory[player.current_weapon_index]

    if not paused:
        player.update(keys, enemies, platforms, len(level_map) * tile_size)
        for enemy in enemies:
            enemy.update(player, enemies, platforms)



    # Cálculo do offset da câmara
    offset_x = player.rect.x - SCREEN_WIDTH // 2
    offset_y = player.rect.y - SCREEN_HEIGHT // 2

    screen.fill(BLACK)

    for platform in platforms:
        platform.draw(screen, offset_x, offset_y)

    for enemy in enemies:
        enemy.draw(screen, offset_x, offset_y)
        # Desenhar vida do inimigo
        enemy_health_text = font.render(f'{enemy.health}', True, RED)
        screen.blit(enemy_health_text, (enemy.rect.x - offset_x, enemy.rect.y - 20 - offset_y))

    player.draw(screen, offset_x, offset_y)

    # Desenhar vida do jogador
    player_health_text = font.render(f'Vida: {player.health}/{player.max_health}', True, RED)
    screen.blit(player_health_text, (20, 20))

    if paused:
        menu.draw(screen)

    pygame.display.flip()

pygame.quit()
