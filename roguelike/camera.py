from .constants import *

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def update(self, target):
        # Center the camera on the target
        self.x = target.rect.centerx - WINDOW_WIDTH // 2
        self.y = target.rect.centery - WINDOW_HEIGHT // 2
        
    def apply(self, entity):
        # Return a new rect moved by camera offset
        return entity.rect.move(-self.x, -self.y)
