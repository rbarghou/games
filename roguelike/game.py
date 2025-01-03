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
        
        # Spawn player in the first room
        first_room = self.map_gen.rooms[0]
        spawn_x = first_room.center_x * TILE_SIZE
        spawn_y = first_room.center_y * TILE_SIZE
        self.player = Player(spawn_x, spawn_y)
        
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.handle_attack()
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                self.handle_attack()
            self.player.handle_event(event)
            
    def handle_attack(self):
        attack_rect = self.player.attack()
        for monster in list(self.monsters):  # Create list copy since we'll modify group
            if attack_rect.colliderect(monster.rect):
                if monster.take_damage(10):  # Deal 10 damage
                    self.monsters.remove(monster)
    
    def update(self):
        self.player.update(self.game_map)
        self.monsters.update(self.player, self.game_map)
        self.camera.update(self.player)
        
        # Update field of view
        player_tile_x = self.player.rect.centerx // TILE_SIZE
        player_tile_y = self.player.rect.centery // TILE_SIZE
        self.game_map.compute_fov(player_tile_x, player_tile_y, FOV_RADIUS)
        
    def draw(self):
        self.screen.fill(BLACK)
        self.game_map.draw(self.screen, self.camera)
        
        # Draw player with camera offset, attack effect, and health bar
        player_rect = self.camera.apply(self.player)
        self.screen.blit(self.player.image, player_rect)
        self.player.draw_attack_effect(self.screen, (self.camera.x, self.camera.y))
        self.player.draw(self.screen)  # This draws the health bar
        
        # Draw only visible monsters with camera offset and health bars
        for monster in self.monsters:
            monster_tile_x = monster.rect.centerx // TILE_SIZE
            monster_tile_y = monster.rect.centery // TILE_SIZE
            
            # Only draw if monster's position is visible
            if (0 <= monster_tile_x < self.game_map.width and 
                0 <= monster_tile_y < self.game_map.height and 
                self.game_map.visible[monster_tile_x][monster_tile_y]):
                monster_rect = self.camera.apply(monster)
                self.screen.blit(monster.image, monster_rect)
                monster.draw_health_bar(self.screen, (self.camera.x, self.camera.y))
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
