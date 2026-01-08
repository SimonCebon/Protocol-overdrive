import pygame
import sys
from settings import *
from sprites import Player
from managers import SpawnManager

class Game:
    def __init__(self):
        """Initialize the game window and systems."""
        pygame.init()
        # Double buffering to reduce flickering
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize Font for UI
        self.font = pygame.font.SysFont("arial", 20, bold=True)

        # 1. Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group() # New Group for bullets

        # 2. Entities
        # Player needs to know about projectiles (to shoot them) and enemies (to aim at them)
        self.player = Player(
            groups=[self.all_sprites], 
            projectile_groups=[self.all_sprites, self.projectiles], 
            enemy_group=self.enemies
        )
        
        # 3. Managers
        self.spawn_manager = SpawnManager(self.player, [self.all_sprites, self.enemies])

    def run(self):
        """The main game loop."""
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def update(self):
        """Update game state."""
        self.all_sprites.update(self.dt)
        self.spawn_manager.update(self.dt)
        
        # NEW: Check Collision
        self.check_collisions()
        
    def check_collisions(self):
        """Handle interactions between sprites."""
        # 1. Projectiles vs Enemies
        # groupcollide(groupA, groupB, dokillA, dokillB)
        # We don't want to kill enemies instantly (they have HP), so dokillB=False
        hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True)
        
        for enemy, projectiles_hit in hits.items():
            # Apply damage for every bullet that hit this enemy
            for proj in projectiles_hit:
                enemy.health -= PROJECTILE_DAMAGE
                
                # Check Death
                if enemy.health <= 0:
                    enemy.kill() # Remove from all groups
                    
                    # Add Charge to Player
                    # Cap is 8.0. Math: min(current + gain, max)
                    self.player.charge = min(self.player.charge + CHARGE_PER_HIT, CHARGE_CAP)

        # 2. Enemies vs Player
        # collide_mask or collide_rect checks if player touches enemy
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            self.player.health -= 1 # Drain HP on contact
            if self.player.health <= 0:
                print("GAME OVER")
                self.running = False


    def draw_ui(self):
        """Draw Health and Charge bars."""
        # A. Health Bar (Top Left)
        # Background (Red)
        pygame.draw.rect(self.screen, (100, 0, 0), (10, 10, 200, 20))
        # Foreground (Green) - Width based on %
        hp_ratio = max(self.player.health / PLAYER_HP, 0)
        pygame.draw.rect(self.screen, (0, 200, 0), (10, 10, 200 * hp_ratio, 20))
        # Border (White)
        pygame.draw.rect(self.screen, COLOR_WHITE, (10, 10, 200, 20), 2)
        
        # B. Charge Bar (Bottom Center)
        # We want 8 discrete boxes
        bar_width = 40
        bar_height = 20
        start_x = (SCREEN_WIDTH // 2) - ((bar_width * 8) // 2)
        y = SCREEN_HEIGHT - 40
        
        for i in range(8):
            rect_x = start_x + (i * bar_width)
            # Draw frame
            pygame.draw.rect(self.screen, COLOR_WHITE, (rect_x, y, bar_width, bar_height), 2)
            
            # Draw fill
            # Logic: If we have 3.5 charge:
            # Box 0, 1, 2 are FULL. Box 3 is HALF. Box 4+ are EMPTY.
            if self.player.charge >= i + 1:
                fill_pct = 1.0
            elif self.player.charge > i:
                fill_pct = self.player.charge - i # Fractional part
            else:
                fill_pct = 0.0
            
            if fill_pct > 0:
                # Fill with Blue (Cyan)
                fill_width = (bar_width - 4) * fill_pct # -4 for padding
                pygame.draw.rect(self.screen, (0, 255, 255), (rect_x + 2, y + 2, fill_width, bar_height - 4))


    def draw(self):
        """Render everything to the screen."""
        self.screen.fill(COLOR_BLACK)
        
        self.all_sprites.draw(self.screen)
        
        # Movement Target
        if self.player.pos.distance_to(self.player.target_pos) > 5:
            target = self.player.target_pos
            pygame.draw.line(self.screen, COLOR_WHITE, (target.x - 5, target.y), (target.x + 5, target.y), 2)
            pygame.draw.line(self.screen, COLOR_WHITE, (target.x, target.y - 5), (target.x, target.y + 5), 2)

        # UI
        self.draw_ui()
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
