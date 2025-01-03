import pygame
import random
from .constants import *

class Rect:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        
    @property
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)
    
    @property
    def center_x(self):
        return (self.x1 + self.x2) // 2
        
    @property
    def center_y(self):
        return (self.y1 + self.y2) // 2
    
    def intersects(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[True for y in range(height)] for x in range(width)]  # True = wall
        self.visible = [[False for y in range(height)] for x in range(width)]
        self.explored = [[False for y in range(height)] for x in range(width)]
        
    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y]
        return True
        
    def compute_fov(self, x, y, radius):
        # Reset visibility
        for i in range(self.width):
            for j in range(self.height):
                self.visible[i][j] = False
                
        # Ray casting in all directions
        for angle in range(0, 360, 5):  # Cast a ray every 5 degrees
            self._cast_ray(x, y, angle, radius)
            
    def _cast_ray(self, start_x, start_y, angle, max_distance):
        import math
        
        # Convert angle to radians
        rad = math.radians(angle)
        
        # Calculate direction vector
        dx = math.cos(rad)
        dy = math.sin(rad)
        
        # Start position (in tile coordinates)
        x = float(start_x)
        y = float(start_y)
        
        # Mark starting position as visible
        self.visible[int(x)][int(y)] = True
        self.explored[int(x)][int(y)] = True
        
        # Cast the ray
        for distance in range(max_distance):
            # Move along the ray
            x += dx
            y += dy
            
            # Convert to integer coordinates
            tile_x = int(x)
            tile_y = int(y)
            
            # Stop if out of bounds
            if not (0 <= tile_x < self.width and 0 <= tile_y < self.height):
                break
                
            # Mark tile as visible and explored
            self.visible[tile_x][tile_y] = True
            self.explored[tile_x][tile_y] = True
            
            # Stop at walls
            if self.tiles[tile_x][tile_y]:
                break
        
    def draw(self, screen, camera):
        # Calculate visible range based on camera position
        start_x = max(0, camera.x // TILE_SIZE)
        end_x = min(self.width, (camera.x + WINDOW_WIDTH) // TILE_SIZE + 1)
        start_y = max(0, camera.y // TILE_SIZE)
        end_y = min(self.height, (camera.y + WINDOW_HEIGHT) // TILE_SIZE + 1)
        
        # Only draw explored tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if self.explored[x][y]:
                    if self.tiles[x][y]:  # Wall
                        color = VISIBLE_COLOR if self.visible[x][y] else UNSEEN_COLOR
                        pygame.draw.rect(screen, color,
                                       (x * TILE_SIZE - camera.x,
                                        y * TILE_SIZE - camera.y,
                                        TILE_SIZE, TILE_SIZE))

class MapGenerator:
    def __init__(self):
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        self.rooms = []
        
    def create_room(self, room):
        # Set tiles in room area to floor (False)
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.game_map.tiles[x][y] = False
                
    def create_tunnel(self, start, end):
        x1, y1 = start
        x2, y2 = end
        
        # Horizontal tunnel
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.game_map.tiles[x][y1] = False
            
        # Vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.game_map.tiles[x2][y] = False
            
    def generate(self):
        for _ in range(MAX_ROOMS):
            width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, MAP_WIDTH - width - 1)
            y = random.randint(0, MAP_HEIGHT - height - 1)
            
            new_room = Rect(x, y, width, height)
            
            if not any(new_room.intersects(other) for other in self.rooms):
                self.create_room(new_room)
                
                if self.rooms:  # Connect to previous room
                    prev_room = self.rooms[-1]
                    self.create_tunnel(prev_room.center, new_room.center)
                    
                self.rooms.append(new_room)
                
        return self.game_map
