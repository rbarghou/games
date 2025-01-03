import pygame
import random
import numpy as np
from pygame import mixer
from array import array

# Initialize Pygame and mixer
pygame.init()
mixer.init(frequency=44100, size=-16, channels=1)

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
SAMPLE_RATE = 44100

# Colors and game settings (unchanged)
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
    return array('h', wave)

def create_match_sound():
    # Cheerful ascending arpeggio
    sound_data = generate_sine_wave(440, 0.1)  # A4
    sound_data.extend(generate_sine_wave(554.37, 0.1))  # C#5
    sound_data.extend(generate_sine_wave(659.25, 0.1))  # E5
    sound = pygame.mixer.Sound(buffer=sound_data)
    return sound

def create_fail_sound():
    # Descending minor second
    sound_data = generate_sine_wave(440, 0.1)  # A4
    sound_data.extend(generate_sine_wave(415.30, 0.2))  # Ab4
    sound = pygame.mixer.Sound(buffer=sound_data)
    return sound

def create_combo_sound():
    # Rising power chord
    sound_data = generate_sine_wave(440, 0.1)  # A4
    sound_data.extend(generate_sine_wave(659.25, 0.1))  # E5
    sound_data.extend(generate_sine_wave(880, 0.2))  # A5
    sound = pygame.mixer.Sound(buffer=sound_data)
    return sound

class ColorMatch:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Color Match")
        self.clock = pygame.time.Clock()
        
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
        
        # Font
        self.font = pygame.font.Font(None, 36)
        
    # Rest of the class methods remain unchanged
    def new_target(self):
        color_index = random.randint(0, len(COLORS) - 1)
        name_index = random.randint(0, len(COLOR_NAMES) - 1)
        self.target_color = COLORS[color_index]
        self.target_color_name = COLOR_NAMES[name_index]
        
    def spawn_falling_color(self):
        if random.random() < 0.02 * self.speed:
            color = random.choice(COLORS)
            x = random.randint(0, WINDOW_WIDTH - 30)
            self.falling_colors.append({"color": color, "pos": [x, -30]})
            
    def update_falling_colors(self):
        for color in self.falling_colors[:]:
            color["pos"][1] += self.speed
            if color["pos"][1] > WINDOW_HEIGHT:
                self.falling_colors.remove(color)
                if color["color"] == self.target_color:
                    self.fail_sound.play()
                    self.combo = 0
                    if self.score > 0:
                        self.score -= 1
                        
    def handle_click(self, pos):
        for color in self.falling_colors[:]:
            x, y = color["pos"]
            if (x < pos[0] < x + 30 and 
                y < pos[1] < y + 30):
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
            pygame.draw.rect(self.screen, color["color"], 
                           (color["pos"][0], color["pos"][1], 30, 30))
        
        # Draw target color name
        text = self.font.render(self.target_color_name, True, self.target_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, 50))
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                    
            self.spawn_falling_color()
            self.update_falling_colors()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = ColorMatch()
    game.run()
