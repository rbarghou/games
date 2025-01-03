import pygame
from constants import *


class Shop:
    def __init__(self, game):
        self.game = game
        self.selected_item = 0
        self.upgrades = {
            "extra_lives": 0,
            "speed_reduction": 0,
            "combo_time": 0,
            "point_multiplier": 0,
        }

    def draw(self, screen, font):
        screen.fill(BLACK)

        # Draw header
        header = font.render(f"SHOP - Credits: {self.game.credits}", True, GOLD)
        screen.blit(header, (20, 20))

        # Draw items
        for i, item in enumerate(SHOP_ITEMS):
            color = WHITE if i == self.selected_item else GRAY
            text = font.render(f"{item['name']} - {item['cost']} credits", True, color)
            desc = font.render(item["description"], True, color)
            screen.blit(text, (20, 100 + i * 60))
            screen.blit(desc, (20, 120 + i * 60))

        # Draw instructions
        instructions = font.render("↑↓: Select   SPACE: Buy   R: Restart", True, WHITE)
        screen.blit(instructions, (20, WINDOW_HEIGHT - 40))

        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(SHOP_ITEMS)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(SHOP_ITEMS)
            elif event.key == pygame.K_SPACE:
                self.buy_item()
            elif event.key == pygame.K_r:
                return "restart"
        return None

    def buy_item(self):
        item = SHOP_ITEMS[self.selected_item]
        if self.game.credits >= item["cost"]:
            self.game.credits -= item["cost"]
            if item["name"] == "Extra Life":
                self.upgrades["extra_lives"] += 1
            elif item["name"] == "Speed Down":
                self.upgrades["speed_reduction"] += 0.2
            elif item["name"] == "Combo Time":
                self.upgrades["combo_time"] += 1
            elif item["name"] == "Point Bonus":
                self.upgrades["point_multiplier"] += 0.5
            self.game.sound_manager.match_sound.play()
        else:
            self.game.sound_manager.fail_sound.play()
