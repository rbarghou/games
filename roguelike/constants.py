import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
TILE_SIZE = 32
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Player settings
PLAYER_SPEED = 5
PLAYER_HP = 100
ATTACK_RANGE = 50  # pixels

# Map settings
MAP_WIDTH = 50
MAP_HEIGHT = 50
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# Health bar settings
HEALTH_BAR_WIDTH = 30
HEALTH_BAR_HEIGHT = 5
HEALTH_BAR_OFFSET = 5  # pixels above entity

# Attack effect settings
ATTACK_EFFECT_DURATION = 200  # milliseconds
ATTACK_EFFECT_COLOR = (255, 255, 0)  # Yellow

# Monster settings
MONSTER_ATTACK_RANGE = 40  # pixels
MONSTER_ATTACK_DAMAGE = 5
MONSTER_ATTACK_COOLDOWN = 1000  # milliseconds

# Field of View settings
FOV_RADIUS = 8  # tiles
FOV_LIGHT_WALLS = True
VISIBLE_COLOR = (200, 200, 200)  # Light gray for visible walls
UNSEEN_COLOR = (30, 30, 30)    # Dark gray for unseen areas
