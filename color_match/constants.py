# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Player settings
PLAYER_SPEED = 7
PLAYER_SIZE = 40
INITIAL_LIVES = 3

# Game settings
INITIAL_SPEED = 2
SPEED_INCREMENT = 0.2
COMBO_THRESHOLD = 3
COMBO_TIMEOUT = FPS * 3  # 3 seconds

# Colors and text
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
COLOR_NAMES = ["RED", "GREEN", "BLUE", "YELLOW"]

# Shop items
SHOP_ITEMS = [
    {"name": "Extra Life", "cost": 1000, "description": "Add one life"},
    {"name": "Speed Down", "cost": 800, "description": "Reduce game speed by 20%"},
    {"name": "Combo Time", "cost": 500, "description": "Increase combo timer"},
    {"name": "Point Bonus", "cost": 1500, "description": "Earn 50% more credits"}
]