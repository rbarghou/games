import pygame
import random
from constants import *
from player import Player
from sound_manager import SoundManager
from shop import Shop

class ColorMatch:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Color Match")
        self.clock = pygame.time.Clock()
        
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joy in joysticks:
            joy.init()
        
        self.sound_manager = SoundManager()
        self.shop = Shop(self)
        self.credits = 0
        self.reset_game()
        self.font = pygame.font.Font(None, 36)
        self.next_target = None
        
    def reset_game(self):
        self.score = 0
        self.credits = self.credits if hasattr(self, 'credits') else 0
        self.combo = 0
        self.combo_timer = 0
        self.speed = INITIAL_SPEED * (1 - self.shop.upgrades["speed_reduction"])
        self.falling_colors = []
        self.target_color = None
        self.target_color_name = None
        self.game_over = False
        self.in_shop = False
        self.player = Player(WINDOW_WIDTH//2, WINDOW_HEIGHT - 100, 
                           self.shop.upgrades["player_width"])
        self.player.lives += self.shop.upgrades["extra_lives"]
        self.next_target = None
        
    def new_target(self):
        if self.shop.upgrades["color_preview"] > 0 and self.next_target:
            self.target_color, self.target_color_name = self.next_target
            
        color_index = random.randint(0, len(COLORS) - 1)
        name_index = random.randint(0, len(COLOR_NAMES) - 1)
        
        if self.shop.upgrades["color_preview"] > 0:
            self.next_target = (COLORS[color_index], COLOR_NAMES[name_index])
        else:
            self.target_color = COLORS[color_index]
            self.target_color_name = COLOR_NAMES[name_index]
            
    def spawn_falling_color(self):
        if random.random() < 0.02 * self.speed:
            color = random.choice(COLORS)
            x = random.randint(0, WINDOW_WIDTH - 30)
            self.falling_colors.append({
                "color": color, 
                "rect": pygame.Rect(x, -30, 30, 30)
            })
            
    def update_falling_colors(self):
        for color in self.falling_colors[:]:
            color["rect"].y += self.speed
            if color["rect"].y > WINDOW_HEIGHT:
                self.falling_colors.remove(color)
            
            if color["rect"].colliderect(self.player.rect):
                self.falling_colors.remove(color)
                if color["color"] == self.target_color:
                    self.sound_manager.match_sound.play()
                    base_points = int(10 * (1 + self.combo * 0.5 * (1 + self.shop.upgrades["combo_rate"])) 
                                    * (self.speed / INITIAL_SPEED))
                    multiplier = 1 + self.shop.upgrades["point_multiplier"]
                    self.score += base_points
                    self.credits += int(base_points * multiplier)
                    self.combo_timer = 0
                    self.combo += 1
                    if self.combo >= COMBO_THRESHOLD:
                        self.sound_manager.combo_sound.play()
                    self.speed += SPEED_INCREMENT
                else:
                    if self.player.invulnerable == 0:
                        if random.random() > self.shop.upgrades["safety_net"]:
                            self.sound_manager.fail_sound.play()
                            self.player.lives -= 1
                            if self.player.lives > 0:
                                self.player.invulnerable = FPS * 2
                    self.combo = 0

    def draw_lives(self):
        for i in range(self.player.lives):
            pygame.draw.rect(self.screen, RED, 
                           (10 + i * 30, WINDOW_HEIGHT - 40, 20, 20))
                        
    def draw(self):
        self.screen.fill(BLACK)
        
        for color in self.falling_colors:
            pygame.draw.rect(self.screen, color["color"], color["rect"])
        
        if self.player.invulnerable == 0 or self.player.invulnerable % 10 < 5:
            pygame.draw.rect(self.screen, WHITE, self.player.rect)
        
        text = self.font.render(self.target_color_name, True, self.target_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, 50))
        self.screen.blit(text, text_rect)
        
        if self.next_target and self.shop.upgrades["color_preview"] > 0:
            preview = self.font.render("Next: " + self.next_target[1], True, self.next_target[0])
            self.screen.blit(preview, (WINDOW_WIDTH - 150, 50))
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        credits_text = self.font.render(f"Credits: {self.credits}", True, GOLD)
        combo_text = self.font.render(f"Combo: {self.combo}x", True, WHITE)
        speed_text = self.font.render(f"Speed: {self.speed:.1f}x", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(credits_text, (10, 40))
        self.screen.blit(combo_text, (10, 70))
        self.screen.blit(speed_text, (10, 100))
        
        self.draw_lives()
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press SPACE to enter shop", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        
    def run(self):
        self.new_target()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.in_shop:
                    result = self.shop.handle_input(event)
                    if result == "restart":
                        self.in_shop = False
                        self.reset_game()
                        self.new_target()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.in_shop = True
            
            if self.in_shop:
                self.shop.draw(self.screen, self.font)
            elif not self.game_over:
                if self.player.lives <= 0:
                    self.game_over = True
                else:
                    self.player.update()
                    self.spawn_falling_color()
                    self.update_falling_colors()
                    
                    # Update combo timer with upgrade
                    self.combo_timer += 1
                    timeout = COMBO_TIMEOUT * (1 + self.shop.upgrades["combo_time"])
                    if self.combo_timer >= timeout:
                        self.combo = 0
                        self.combo_timer = 0
                
                self.draw()
            else:
                self.draw()
            
            self.clock.tick(FPS)
            
        pygame.quit()