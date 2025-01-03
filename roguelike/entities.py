import pygame
import random
from .constants import *

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.hp = 30
        
    def update(self, player, game_map):
        # Simple AI: Move randomly
        dx = random.choice([-1, 0, 1]) * self.speed
        dy = random.choice([-1, 0, 1]) * self.speed
        
        # Test x movement
        self.rect.x += dx
        if self.check_collision(game_map):
            self.rect.x -= dx
            
        # Test y movement
        self.rect.y += dy
        if self.check_collision(game_map):
            self.rect.y -= dy
            
    def check_collision(self, game_map):
        return game_map.is_wall(self.rect.centerx // TILE_SIZE, 
                              self.rect.centery // TILE_SIZE)
                              
    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0  # Return True if monster dies
