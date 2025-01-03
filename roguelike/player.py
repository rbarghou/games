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
        self.attack_effect_time = 0
        self.facing = 'right'  # Can be: 'left', 'right', 'up', 'down'
        
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
        
        # Update facing direction based on movement
        if dx > 0:
            self.facing = 'right'
        elif dx < 0:
            self.facing = 'left'
        if dy > 0:
            self.facing = 'down'
        elif dy < 0:
            self.facing = 'up'

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
        # Start attack effect timer
        self.attack_effect_time = pygame.time.get_ticks()
        
        # Create directional attack rectangle based on facing direction
        if self.facing == 'right':
            return pygame.Rect(
                self.rect.right,
                self.rect.centery - ATTACK_RANGE//2,
                ATTACK_RANGE,
                ATTACK_RANGE
            )
        elif self.facing == 'left':
            return pygame.Rect(
                self.rect.left - ATTACK_RANGE,
                self.rect.centery - ATTACK_RANGE//2,
                ATTACK_RANGE,
                ATTACK_RANGE
            )
        elif self.facing == 'up':
            return pygame.Rect(
                self.rect.centerx - ATTACK_RANGE//2,
                self.rect.top - ATTACK_RANGE,
                ATTACK_RANGE,
                ATTACK_RANGE
            )
        else:  # down
            return pygame.Rect(
                self.rect.centerx - ATTACK_RANGE//2,
                self.rect.bottom,
                ATTACK_RANGE,
                ATTACK_RANGE
            )
        
    def draw_attack_effect(self, screen, camera_offset):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_effect_time < ATTACK_EFFECT_DURATION:
            # Draw directional attack effect
            if self.facing == 'right':
                pygame.draw.rect(screen, ATTACK_EFFECT_COLOR,
                    (self.rect.right - camera_offset[0],
                     self.rect.centery - ATTACK_RANGE//2 - camera_offset[1],
                     ATTACK_RANGE,
                     ATTACK_RANGE), 2)
            elif self.facing == 'left':
                pygame.draw.rect(screen, ATTACK_EFFECT_COLOR,
                    (self.rect.left - ATTACK_RANGE - camera_offset[0],
                     self.rect.centery - ATTACK_RANGE//2 - camera_offset[1],
                     ATTACK_RANGE,
                     ATTACK_RANGE), 2)
            elif self.facing == 'up':
                pygame.draw.rect(screen, ATTACK_EFFECT_COLOR,
                    (self.rect.centerx - ATTACK_RANGE//2 - camera_offset[0],
                     self.rect.top - ATTACK_RANGE - camera_offset[1],
                     ATTACK_RANGE,
                     ATTACK_RANGE), 2)
            else:  # down
                pygame.draw.rect(screen, ATTACK_EFFECT_COLOR,
                    (self.rect.centerx - ATTACK_RANGE//2 - camera_offset[0],
                     self.rect.bottom - camera_offset[1],
                     ATTACK_RANGE,
                     ATTACK_RANGE), 2)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        # Draw direction indicator
        indicator_size = 8
        if self.facing == 'right':
            pygame.draw.rect(screen, WHITE, (self.rect.right - indicator_size, 
                                           self.rect.centery - indicator_size//2,
                                           indicator_size, indicator_size))
        elif self.facing == 'left':
            pygame.draw.rect(screen, WHITE, (self.rect.left, 
                                           self.rect.centery - indicator_size//2,
                                           indicator_size, indicator_size))
        elif self.facing == 'up':
            pygame.draw.rect(screen, WHITE, (self.rect.centerx - indicator_size//2,
                                           self.rect.top,
                                           indicator_size, indicator_size))
        elif self.facing == 'down':
            pygame.draw.rect(screen, WHITE, (self.rect.centerx - indicator_size//2,
                                           self.rect.bottom - indicator_size,
                                           indicator_size, indicator_size))
