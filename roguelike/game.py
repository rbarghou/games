import pygame
import random
from .constants import *
from .player import Player
from .map_generator import MapGenerator
from .entities import Monster
from .camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Roguelike Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize joysticks
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joy in self.joysticks:
            joy.init()
        
        self.map_gen = MapGenerator()
        self.game_map = self.map_gen.generate()
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.monsters = pygame.sprite.Group()
        self.camera = Camera()
        self.spawn_monsters()
        
    def spawn_monsters(self):
        for room in self.map_gen.rooms:
            if random.random() < 0.7:  # 70% chance to spawn monster in room
                x = room.center_x * TILE_SIZE
                y = room.center_y * TILE_SIZE
                monster = Monster(x, y)
                self.monsters.add(monster)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_event(event)
    
    def update(self):
        self.player.update(self.game_map)
        self.monsters.update(self.player, self.game_map)
        self.camera.update(self.player)
        
    def draw(self):
        self.screen.fill(BLACK)
        self.game_map.draw(self.screen, self.camera)
        
        # Draw player with camera offset
        player_rect = self.camera.apply(self.player)
        self.screen.blit(self.player.image, player_rect)
        
        # Draw monsters with camera offset
        for monster in self.monsters:
            monster_rect = self.camera.apply(monster)
            self.screen.blit(monster.image, monster_rect)
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
