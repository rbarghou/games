import pygame
import random
import numpy as np
from pygame import mixer
from array import array

pygame.init()
mixer.init(frequency=44100, size=-16, channels=1)

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
SAMPLE_RATE = 44100
PLAYER_SPEED = 7
PLAYER_SIZE = 40

# Colors and game settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
COLOR_NAMES = ["RED", "GREEN", "BLUE", "YELLOW"]
INITIAL_SPEED = 2
SPEED_INCREMENT = 0.2
COMBO_THRESHOLD = 3


def generate_sine_wave(frequency, duration, volume=0.5):
    num_samples = int(SAMPLE_RATE * duration)
    samples = np.arange(num_samples)
    wave = np.sin(2 * np.pi * frequency * samples / SAMPLE_RATE)
    wave = (wave * volume * 32767).astype(np.int16)
    return array("h", wave)


def create_match_sound():
    sound_data = generate_sine_wave(440, 0.1)
    sound_data.extend(generate_sine_wave(554.37, 0.1))
    sound_data.extend(generate_sine_wave(659.25, 0.1))
    return pygame.mixer.Sound(buffer=sound_data)


def create_fail_sound():
    sound_data = generate_sine_wave(440, 0.1)
    sound_data.extend(generate_sine_wave(415.30, 0.2))
    return pygame.mixer.Sound(buffer=sound_data)


def create_combo_sound():
    sound_data = generate_sine_wave(440, 0.1)
    sound_data.extend(generate_sine_wave(659.25, 0.1))
    sound_data.extend(generate_sine_wave(880, 0.2))
    return pygame.mixer.Sound(buffer=sound_data)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        self.velocity_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.velocity_y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        # Get gamepad input if available
        joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        if joysticks:
            joy = joysticks[0]
            self.velocity_x += joy.get_axis(0) * self.speed
            self.velocity_y += joy.get_axis(1) * self.speed

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Keep player in bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))


class ColorMatch:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Color Match")
        self.clock = pygame.time.Clock()

        # Initialize joysticks
        pygame.joystick.init()
        joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        for joy in joysticks:
            joy.init()

        # Generate sounds
        self.match_sound = create_match_sound()
        self.fail_sound = create_fail_sound()
        self.combo_sound = create_combo_sound()

        # Game state
        self.score = 0
        self.combo = 0
        self.speed = INITIAL_SPEED
        self.falling_colors = []
        self.target_color = None
        self.target_color_name = None
        self.game_over = False
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)

        # Font
        self.font = pygame.font.Font(None, 36)

    def new_target(self):
        color_index = random.randint(0, len(COLORS) - 1)
        name_index = random.randint(0, len(COLOR_NAMES) - 1)
        self.target_color = COLORS[color_index]
        self.target_color_name = COLOR_NAMES[name_index]

    def spawn_falling_color(self):
        if random.random() < 0.02 * self.speed:
            color = random.choice(COLORS)
            x = random.randint(0, WINDOW_WIDTH - 30)
            self.falling_colors.append(
                {"color": color, "rect": pygame.Rect(x, -30, 30, 30)}
            )

    def update_falling_colors(self):
        for color in self.falling_colors[:]:
            color["rect"].y += self.speed
            if color["rect"].y > WINDOW_HEIGHT:
                self.falling_colors.remove(color)
                if color["color"] == self.target_color:
                    self.fail_sound.play()
                    self.combo = 0
                    if self.score > 0:
                        self.score -= 1

            # Check collision with player
            if color["rect"].colliderect(self.player.rect):
                self.falling_colors.remove(color)
                if color["color"] == self.target_color:
                    self.match_sound.play()
                    self.score += 1 + self.combo
                    self.combo += 1
                    if self.combo >= COMBO_THRESHOLD:
                        self.combo_sound.play()
                    self.speed += SPEED_INCREMENT
                else:
                    self.fail_sound.play()
                    self.combo = 0
                    if self.score > 0:
                        self.score -= 1

    def draw(self):
        self.screen.fill(BLACK)

        # Draw falling colors
        for color in self.falling_colors:
            pygame.draw.rect(self.screen, color["color"], color["rect"])

        # Draw player
        pygame.draw.rect(self.screen, WHITE, self.player.rect)

        # Draw target color name
        text = self.font.render(self.target_color_name, True, self.target_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 50))
        self.screen.blit(text, text_rect)

        # Draw score and combo
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        combo_text = self.font.render(f"Combo: {self.combo}x", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(combo_text, (10, 50))

        pygame.display.flip()

    def run(self):
        self.new_target()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.update()
            self.spawn_falling_color()
            self.update_falling_colors()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = ColorMatch()
    game.run()
