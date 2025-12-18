import pygame
import random
from settings import *
from sprites import StandardEnemy, FastEnemy

class SpawnManager:
    def __init__(self, player, enemy_groups):
        self.player = player
        self.enemy_groups = enemy_groups # Sprite groups to add enemies to
        self.spawn_timer = 0
        self.spawn_interval = 2000 # Spawn every 2 seconds initially

    def get_random_spawn_pos(self):
        """Generate a coordinate outside the screen."""
        spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if spawn_side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = -50
        elif spawn_side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 50
        elif spawn_side == 'left':
            x = -50
            y = random.randint(0, SCREEN_HEIGHT)
        else: # right
            x = SCREEN_WIDTH + 50
            y = random.randint(0, SCREEN_HEIGHT)
            
        return pygame.math.Vector2(x, y)

    def spawn(self):
        """Create a new enemy instance."""
        pos = self.get_random_spawn_pos()
        
        # 20% chance for a Fast Enemy
        if random.random() < 0.2:
            enemy = FastEnemy(self.enemy_groups, self.player)
        else:
            enemy = StandardEnemy(self.enemy_groups, self.player)
            
        enemy.pos = pos
        enemy.rect.center = round(pos.x), round(pos.y)

    def update(self, dt):
        """Handle spawn timing."""
        self.spawn_timer += dt * 1000 # Convert dt (seconds) to milliseconds
        
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn()
