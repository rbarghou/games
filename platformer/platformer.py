import pygame
import sys
import random

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CHUNK_SIZE = 800
FPS = 60
GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Camera:
    def __init__(self):
        self.offset_x = 0
    
    def apply(self, entity):
        return entity.rect.move(-self.offset_x, 0)
    
    def update(self, target):
        self.offset_x = target.rect.centerx - WINDOW_WIDTH // 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jumping = False
        self.start_x = x

    def update(self, platforms):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.jumping = False
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.velocity_y = 0
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_SPEED
            self.jumping = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class World:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.chunks = {}
        self.generate_initial_chunks()

    def generate_chunk(self, chunk_x):
        if chunk_x not in self.chunks:
            platforms = []
            chunk_start_x = chunk_x * CHUNK_SIZE
            
            # Generate 3-5 platforms per chunk
            for _ in range(random.randint(3, 5)):
                width = random.randint(100, 200)
                x = chunk_start_x + random.randint(0, CHUNK_SIZE - width)
                y = random.randint(200, 500)
                platform = Platform(x, y, width, 20)
                platforms.append(platform)
                self.platforms.add(platform)
            
            self.chunks[chunk_x] = platforms

    def generate_initial_chunks(self):
        for i in range(-2, 3):
            self.generate_chunk(i)

    def update(self, camera_x):
        current_chunk = camera_x // CHUNK_SIZE
        
        # Generate new chunks ahead
        for i in range(current_chunk - 2, current_chunk + 3):
            self.generate_chunk(i)
        
        # Remove far chunks
        chunks_to_remove = []
        for chunk_x in self.chunks:
            if abs(chunk_x - current_chunk) > 3:
                chunks_to_remove.append(chunk_x)
        
        for chunk_x in chunks_to_remove:
            for platform in self.chunks[chunk_x]:
                platform.kill()
            del self.chunks[chunk_x]

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Infinite Platformer")
    clock = pygame.time.Clock()

    camera = Camera()
    world = World()
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            player.rect.x += MOVE_SPEED

        # Update
        player.update(world.platforms)
        camera.update(player)
        world.update(camera.offset_x)

        # Draw
        screen.fill(BLACK)
        for sprite in world.platforms:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()