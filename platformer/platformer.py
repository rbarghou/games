import pygame
import sys
import random

pygame.init()

# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CHUNK_SIZE = WINDOW_WIDTH
FPS = 60
GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5
MAX_JUMP_HEIGHT = abs(
    JUMP_SPEED * JUMP_SPEED / (2 * GRAVITY)
)  # Calculate actual max jump height
PLATFORM_MIN_SPACING = 80
PLATFORM_MAX_SPACING = 120

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)


class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, entity):
        return entity.rect.move(-self.offset_x, -self.offset_y)

    def update(self, target):
        self.offset_x = target.rect.centerx - WINDOW_WIDTH // 2
        self.offset_y = max(0, target.rect.centery - WINDOW_HEIGHT // 2)


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
        self.max_jump_height = MAX_JUMP_HEIGHT

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


class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CHUNK_SIZE, 100))
        self.image.fill(BROWN)

        # Add texture pattern
        for _ in range(50):
            x_pos = random.randint(0, CHUNK_SIZE - 20)
            y_pos = random.randint(0, 80)
            pygame.draw.rect(self.image, DARK_BROWN, (x_pos, y_pos, 20, 20))

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, WINDOW_HEIGHT)


class World:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.ground_chunks = pygame.sprite.Group()
        self.chunks = {}
        self.current_height = WINDOW_HEIGHT - 100
        self.last_platform = None
        self.generate_initial_chunks()

    def is_reachable(self, from_platform, to_platform):
        if not from_platform:
            return True

        dx = to_platform.rect.centerx - from_platform.rect.centerx
        dy = from_platform.rect.top - to_platform.rect.bottom

        # Check horizontal distance is within reasonable range
        if abs(dx) > MAX_JUMP_HEIGHT * 2:
            return False

        # Check vertical distance is within jump height
        if dy > MAX_JUMP_HEIGHT:
            return False

        return True

    def generate_chunk(self, chunk_x):
        if chunk_x not in self.chunks:
            # Create ground for this chunk
            ground = Ground(chunk_x * CHUNK_SIZE)
            self.ground_chunks.add(ground)

            platforms = []
            chunk_start_x = chunk_x * CHUNK_SIZE
            x = chunk_start_x

            while x < chunk_start_x + CHUNK_SIZE - 100:  # Leave room for last platform
                width = random.randint(100, 150)
                attempts = 0
                valid_platform = False

                while not valid_platform and attempts < 10:
                    if self.last_platform is None:
                        proposed_height = WINDOW_HEIGHT - 150
                    else:
                        height_change = random.randint(10, 50)  # Reduced height change
                        proposed_height = max(
                            WINDOW_HEIGHT - 400, self.current_height - height_change
                        )

                    platform = Platform(x, proposed_height, width, 20)

                    if self.is_reachable(self.last_platform, platform):
                        valid_platform = True
                        self.current_height = proposed_height
                        platforms.append(platform)
                        self.platforms.add(platform)
                        self.last_platform = platform

                    attempts += 1

                if not valid_platform:
                    # Fallback: Create a safely reachable platform
                    safe_height = min(
                        WINDOW_HEIGHT - 200, self.current_height + MAX_JUMP_HEIGHT // 2
                    )
                    platform = Platform(x, safe_height, width, 20)
                    platforms.append(platform)
                    self.platforms.add(platform)
                    self.last_platform = platform
                    self.current_height = safe_height

                x += random.randint(PLATFORM_MIN_SPACING, PLATFORM_MAX_SPACING) + width

            self.chunks[chunk_x] = platforms

    def generate_initial_chunks(self):
        for i in range(-2, 3):
            self.generate_chunk(i)

    def update(self, camera_x):
        current_chunk = camera_x // CHUNK_SIZE

        for i in range(current_chunk - 2, current_chunk + 3):
            self.generate_chunk(i)

        chunks_to_remove = []
        for chunk_x in self.chunks:
            if abs(chunk_x - current_chunk) > 3:
                chunks_to_remove.append(chunk_x)

        for chunk_x in chunks_to_remove:
            for platform in self.chunks[chunk_x]:
                platform.kill()
            del self.chunks[chunk_x]

            # Remove ground chunks that are far away
            for ground in self.ground_chunks:
                if (
                    ground.rect.x < (current_chunk - 3) * CHUNK_SIZE
                    or ground.rect.x > (current_chunk + 3) * CHUNK_SIZE
                ):
                    ground.kill()


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
                elif event.key == pygame.K_ESCAPE:  # Add escape to exit
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            player.rect.x += MOVE_SPEED

        player.update(world.platforms)
        camera.update(player)
        world.update(camera.offset_x)

        screen.fill(BLACK)
        for ground in world.ground_chunks:
            screen.blit(ground.image, camera.apply(ground))
        for sprite in world.platforms:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
