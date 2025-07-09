import pygame
from config import *

class Enemy:
    def __init__(self, x, y, health=30, color=RED, damage=5, speed=2, patrol_range=100, detection_range=150):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = color
        self.health = health
        self.damage = damage
        self.speed = speed
        self.alive = True

        self.start_x = x
        self.patrol_range = patrol_range
        self.direction = 1

        self.detection_range = detection_range

    def update(self, player, enemies, platforms=None):
        if not self.alive:
            return

        # Calcular distância ao player
        distance_to_player = abs(player.rect.centerx - self.rect.centerx)

        if distance_to_player <= self.detection_range:
            # Seguir player
            if player.rect.centerx > self.rect.centerx:
                self.rect.x += self.speed
            elif player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed
        else:
            # Patrulha
            self.rect.x += self.speed * self.direction
            distance = self.rect.x - self.start_x
            if abs(distance) >= self.patrol_range:
                self.direction *= -1

        # Separação com outros inimigos
        for other in enemies:
            if other is not self and other.alive:
                if self.rect.colliderect(other.rect):
                    # Empurrar um pouco para o lado
                    if self.rect.centerx < other.rect.centerx:
                        self.rect.x -= 1
                    else:
                        self.rect.x += 1

        # Colisão com player
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

        # Verificar morte
        if self.health <= 0:
            self.alive = False

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def draw(self, surface, camera_x=0, camera_y=0):
        if self.alive:
            offset_rect = self.rect.move(-camera_x, -camera_y)
            pygame.draw.rect(surface, self.color, offset_rect)
