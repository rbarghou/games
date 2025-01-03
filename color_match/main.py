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
INITIAL_LIVES = 3

# Colors and game settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
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


def create_lose_life_sound():
    sound_data = generate_sine_wave(220, 0.3, 0.7)
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
        self.lives = INITIAL_LIVES
        self.invulnerable = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.velocity_y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        if joysticks:
            joy = joysticks[0]
            self.velocity_x += joy.get_axis(0) * self.speed
            self.velocity_y += joy.get_axis(1) * self.speed

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        if self.invulnerable > 0:
            self.invulnerable -= 1


class ColorMatch:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Color Match")
        self.clock = pygame.time.Clock()

        pygame.joystick.init()
        joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        for joy in joysticks:
            joy.init()

        self.match_sound = create_match_sound()
        self.fail_sound = create_fail_sound()
        self.combo_sound = create_combo_sound()
        self.lose_life_sound = create_lose_life_sound()

        self.reset_game()
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        self.score = 0
        self.combo = 0
        self.speed = INITIAL_SPEED
        self.falling_colors = []
        self.target_color = None
        self.target_color_name = None
        self.game_over = False
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)

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
                    if self.player.invulnerable == 0:
                        self.lose_life_sound.play()
                        self.player.lives -= 1
                        if self.player.lives > 0:
                            self.player.invulnerable = (
                                FPS * 2
                            )  # 2 seconds invulnerability
                    self.combo = 0

            if color["rect"].colliderect(self.player.rect):
                self.falling_colors.remove(color)
                if color["color"] == self.target_color:
                    self.match_sound.play()
                    self.score += int(
                        10 * (1 + self.combo * 0.5) * (self.speed / INITIAL_SPEED)
                    )
                    self.combo += 1
                    if self.combo >= COMBO_THRESHOLD:
                        self.combo_sound.play()
                    self.speed += SPEED_INCREMENT
                else:
                    if self.player.invulnerable == 0:
                        self.fail_sound.play()
                        self.player.lives -= 1
                        if self.player.lives > 0:
                            self.player.invulnerable = FPS * 2
                    self.combo = 0

    def draw_lives(self):
        for i in range(self.player.lives):
            pygame.draw.rect(
                self.screen, RED, (10 + i * 30, WINDOW_HEIGHT - 40, 20, 20)
            )

    def draw(self):
        self.screen.fill(BLACK)

        for color in self.falling_colors:
            pygame.draw.rect(self.screen, color["color"], color["rect"])

        # Draw player with flashing effect when invulnerable
        if self.player.invulnerable == 0 or self.player.invulnerable % 10 < 5:
            pygame.draw.rect(self.screen, WHITE, self.player.rect)

        text = self.font.render(self.target_color_name, True, self.target_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 50))
        self.screen.blit(text, text_rect)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        combo_text = self.font.render(f"Combo: {self.combo}x", True, WHITE)
        speed_text = self.font.render(f"Speed: {self.speed:.1f}x", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(combo_text, (10, 50))
        self.screen.blit(speed_text, (10, 90))

        self.draw_lives()

        if self.game_over:
            game_over_text = self.font.render(
                "GAME OVER - Press SPACE to restart", True, WHITE
            )
            text_rect = game_over_text.get_rect(
                center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            )
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        self.new_target()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                        self.new_target()

            if not self.game_over:
                if self.player.lives <= 0:
                    self.game_over = True
                else:
                    self.player.update()
                    self.spawn_falling_color()
                    self.update_falling_colors()

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = ColorMatch()
    game.run()
