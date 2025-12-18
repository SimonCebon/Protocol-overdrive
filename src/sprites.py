import pygame
import random
from settings import *

class Entity(pygame.sprite.Sprite):
    """Base class for all moving objects."""
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, 0)
        self.speed = 0

class Player(Entity):
    def __init__(self, groups):
        super().__init__(groups)
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

    def input(self):
        """Handle mouse input for movement."""
        if pygame.mouse.get_pressed()[0]:  # Left click
            self.target_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    def update(self, dt):
        """Move towards the target position."""
        self.input()
        
        # Vector Math: Direction = Target - Current
        direction = self.target_pos - self.pos
        
        # Only move if we are not already close enough
        if direction.length() > 5:
            direction = direction.normalize() # Scale to length 1
            self.pos += direction * self.speed * dt
            self.rect.center = round(self.pos.x), round(self.pos.y)

class Enemy(Entity):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.image = pygame.Surface((24, 24))
        self.image.fill(COLOR_ENEMY)
        # Spawn logic is handled by manager, but we need a default pos
        self.rect = self.image.get_rect()
        
    def update(self, dt):
        """Chase the player."""
        direction = self.player.pos - self.pos
        if direction.length() > 0: # Avoid division by zero
            direction = direction.normalize()
            self.pos += direction * self.speed * dt
            self.rect.center = round(self.pos.x), round(self.pos.y)

class StandardEnemy(Enemy):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        self.speed = 100   # Standard speed

class FastEnemy(Enemy):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        self.speed = 200   # Fast!
        self.image.fill((255, 100, 100)) # Lighter Red
