import pygame
import random
from settings import *

class Entity(pygame.sprite.Sprite):
    """Base class for all moving objects."""
    def __init__(self, groups):
        # Initialize parent class (pygame.sprite.Sprite)
        super().__init__(groups)
        # Create a surface (image) for the sprite
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        # Use Vector2 for precise float-based position
        self.pos = pygame.math.Vector2(0, 0)
        self.speed = 0

class Projectile(Entity):
    def __init__(self, groups, pos, direction):
        super().__init__(groups)
        self.image = pygame.Surface((8, 8))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.direction = direction.normalize() # Ensure speed is constant
        self.speed = PROJECTILE_SPEED
        self.lifetime = 1000 # Milliseconds

    def update(self, dt):
        # Move: Current Pos + (Direction * Speed * Time)
        self.pos += self.direction * self.speed * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

        # Suicide logic: Die if off-screen or old
        self.lifetime -= dt * 1000
        if self.lifetime <= 0:
            self.kill() # Removes from all groups

class Player(Entity):
    def __init__(self, groups, projectile_groups, enemy_group):
        super().__init__(groups)
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED
        
        # Combat Stats
        self.health = PLAYER_HP
        self.charge = 0.0
        
        # Shooting Setup
        self.projectile_groups = projectile_groups
        self.enemy_group = enemy_group
        self.shoot_timer = 0 # Track time since last shot

    def input(self):
        """Handle mouse input for movement."""
        if pygame.mouse.get_pressed()[0]:  # Left click
            self.target_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    def get_nearest_enemy(self):
        """Find the closest enemy to shoot at."""
        nearest_enemy = None
        min_dist = ATTACK_RANGE # Only look for enemies within range
        
        for enemy in self.enemy_group:
            dist = self.pos.distance_to(enemy.pos)
            if dist < min_dist:
                min_dist = dist
                nearest_enemy = enemy
                
        return nearest_enemy

    def shoot(self):
        """Fire a projectile at the nearest enemy."""
        target = self.get_nearest_enemy()
        if target:
            # Calculate direction to enemy
            direction = target.pos - self.pos
            if direction.length() > 0: # Safety check
                Projectile(self.projectile_groups, self.rect.center, direction)

    def update(self, dt):
        """Move and Shoot."""
        # 1. MOVEMENT
        self.input()
        direction = self.target_pos - self.pos
        if direction.length() > 5:
            direction = direction.normalize()
            self.pos += direction * self.speed * dt
            self.rect.center = round(self.pos.x), round(self.pos.y)
            
        # 2. COMBAT
        self.shoot_timer += dt
        if self.shoot_timer >= ATTACK_COOLDOWN:
            self.shoot()
            self.shoot_timer = 0

class Enemy(Entity):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.image = pygame.Surface((24, 24))
        self.image.fill(COLOR_ENEMY)
        self.rect = self.image.get_rect()
        self.health = 50
        
    def update(self, dt):
        """Chase the player."""
        direction = self.player.pos - self.pos
        if direction.length() > 0: 
            direction = direction.normalize()
            self.pos += direction * self.speed * dt
            self.rect.center = round(self.pos.x), round(self.pos.y)

class StandardEnemy(Enemy):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        self.speed = 100
        self.health = 60

class FastEnemy(Enemy):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        self.speed = 200
        self.health = 30
        self.image.fill((255, 100, 100))
