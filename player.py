import pygame
from config import *
from weapon import Weapon

class Player:
    def __init__(self, x, y):
        self.max_health = 100
        self.health = self.max_health

        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = WHITE
        self.speed = 4
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False
        self.attack_cooldown = 0

        self.inventory = [
            Weapon("Espada rápida", 5, 10, "melee", cooldown=20),
            Weapon("Espada pesada", 15, 30, "melee", cooldown=40),
            Weapon("Arco", 10, 20, "ranged", cooldown=30)
        ]
        self.current_weapon_index = 0
        self.current_weapon = self.inventory[self.current_weapon_index]

    def update(self, keys, enemies, platforms, map_height):
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        if keys[pygame.K_w]:
            pass  # Preparar lógica futura, por exemplo mirar para cima

        self.vel_y += self.gravity
        dy += self.vel_y

        # Colisão com plataformas
        self.on_ground = False
        for platform in platforms:
            if self.rect.move(dx, dy).colliderect(platform.rect):
                if self.rect.bottom <= platform.rect.top + 10 and self.vel_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True

        # Limite inferior (chão do mapa)
        if self.rect.y + dy >= map_height:
            dy = map_height - self.rect.y
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

        # Cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if keys[pygame.K_k] and self.attack_cooldown == 0:
            self.attack(enemies)
            self.attack_cooldown = self.current_weapon.cooldown

        # Verificar colisão com inimigos
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.take_damage(1)  # Exemplo: -1 por frame de contacto

      
        print(f"Player Health: {self.health}/{self.max_health}")
        print(f"Player xy: {self.rect}")

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def attack(self, enemies):
        weapon = self.current_weapon

        # Função de colisão externa
        def check_collision(rect1, rect2):
            return rect1.colliderect(rect2)

        if weapon.range_type == "melee":
            attack_rect = self.rect.copy()
            attack_rect.width += 20
            attack_rect.x += 20  # Ataque para frente (direita por padrão)

            for enemy in enemies[:]:
                if check_collision(attack_rect, enemy.rect):
                    enemy.health -= weapon.damage
                    if enemy.health <= 0:
                        enemies.remove(enemy)

        elif weapon.range_type == "ranged":
            for enemy in enemies[:]:
                if abs(enemy.rect.y - self.rect.y) < 30 and enemy.rect.x > self.rect.x:
                    enemy.health -= weapon.damage
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        # Mostrar arma atual
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Weapon: {self.current_weapon.name}", True, YELLOW)
        surface.blit(text, (10, 10))

    def get_coords(self):
        return (self.rect.x, self.rect.y)
