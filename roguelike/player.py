import pygame
from .constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.hp = PLAYER_HP
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attack()
                
    def update(self, game_map):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        
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
    
    def attack(self):
        # Will implement combat system later
        pass
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
