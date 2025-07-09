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

player = Player(100, 200)
enemies = []
menu = Menu()

# Carregar mapa
current_room = 1
level_map = load_map(current_room)

tile_size = 40
platforms = []

# Passo 1: Criar todas as plataformas
for row_index, row in enumerate(level_map):
    for col_index, cell in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        if cell == "#":
            platforms.append(Platform(x, y, tile_size, 20))

# Passo 2: Criar os inimigos
for row_index, row in enumerate(level_map):
    for col_index, cell in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        if cell == "E":
            enemy = Enemy(x, y)

            # Ajustar inimigo para "pousar" em plataforma
            while not any(enemy.rect.move(0, 1).colliderect(p.rect) for p in platforms):
                enemy.rect.y += 1
                if enemy.rect.y > len(level_map) * tile_size:
                    break

            enemies.append(enemy)

# Altura total do mapa
map_height = len(level_map) * tile_size

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
                    player.current_weapon_index = 0
                    player.current_weapon = player.inventory[0]
                if event.key == pygame.K_2:
                    if len(player.inventory) >= 2:
                        player.current_weapon_index = 1
                        player.current_weapon = player.inventory[1]
                if event.key == pygame.K_3:
                    if len(player.inventory) >= 3:
                        player.current_weapon_index = 2
                        player.current_weapon = player.inventory[2]

    if not game_paused:
        keys = pygame.key.get_pressed()
        player.update(keys, enemies, platforms, map_height)

    for enemy in enemies:
        enemy.update(player, enemies)


    # Calcular offset da câmera
    camera_x = player.rect.centerx - SCREEN_WIDTH // 2
    camera_y = player.rect.centery - SCREEN_HEIGHT // 2

    screen.fill(BLACK)

    for platform in platforms:
        offset_rect = platform.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, platform.color, offset_rect)

    for enemy in enemies:
        offset_rect = enemy.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, enemy.color, offset_rect)

    offset_player = player.rect.move(-camera_x, -camera_y)
    pygame.draw.rect(screen, player.color, offset_player)

    # Mostrar arma
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Weapon: {player.current_weapon.name}", True, YELLOW)
    screen.blit(text, (10, 10))

    if game_paused:
        menu.draw(screen)

    pygame.display.flip()

pygame.quit()
