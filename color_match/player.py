import pygame
from constants import PLAYER_SPEED, PLAYER_SIZE, INITIAL_LIVES, WINDOW_WIDTH, WINDOW_HEIGHT, FPS

class Player:
    def __init__(self, x, y, width_bonus=0):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE + width_bonus, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.velocity_x = 0
        self.velocity_y = 0
        self.lives = INITIAL_LIVES
        self.invulnerable = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.velocity_y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if joysticks:
            joy = joysticks[0]
            self.velocity_x += joy.get_axis(0) * self.speed
            self.velocity_y += joy.get_axis(1) * self.speed

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        
        if self.invulnerable > 0:
            self.invulnerable -= 1