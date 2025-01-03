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
        elif event.type == pygame.JOYBUTTONDOWN:
            # Use button 0 (typically A/X button) for attack
            if event.button == 0:
                self.attack()
                
    def update(self, game_map):
        dx = 0
        dy = 0
        
        # Keyboard controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
            
        # Joystick controls
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            
            # Left analog stick
            dx += joystick.get_axis(0) * self.speed
            dy += joystick.get_axis(1) * self.speed
            
            # D-pad
            dx += joystick.get_hat(0)[0] * self.speed
            dy += joystick.get_hat(0)[1] * self.speed
        
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
