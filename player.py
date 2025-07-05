# player.py

import pygame
from config import *
from weapon import Weapon


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = WHITE
        self.speed = 4
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False
        self.health = 100
        self.attack_cooldown = 0

        # Inventário de armas
        self.inventory = [
            Weapon("Espada rápida", 5, 10, "melee"),
            Weapon("Espada pesada", 15, 30, "melee"),
            Weapon("Arco", 10, 20, "ranged")
        ]
        self.current_weapon_index = 0
        self.current_weapon = self.inventory[self.current_weapon_index]

    def update(self, keys, enemies):
        dx = 0
        dy = 0

        # Movimento
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        # Salto
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        dy += self.vel_y

        # Limite chão
        if self.rect.y + dy >= 500:
            dy = 500 - self.rect.y
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

        # Cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Ataque
        if keys[pygame.K_z] and self.attack_cooldown == 0:
            self.attack(enemies)
            self.attack_cooldown = self.current_weapon.cooldown

    def attack(self, enemies):
        weapon = self.current_weapon
        if weapon.range_type == "melee":
            attack_rect = self.rect.copy()
            attack_rect.width += 20  # alcance lateral
            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.health -= weapon.damage
                    if enemy.health <= 0:
                        enemies.remove(enemy)
        elif weapon.range_type == "ranged":
            # Simulação básica de arco
            for enemy in enemies:
                if abs(enemy.rect.y - self.rect.y) < 30 and enemy.rect.x > self.rect.x:
                    enemy.health -= weapon.damage
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Weapon: {self.current_weapon.name}", True, YELLOW)
        surface.blit(text, (10, 10))
