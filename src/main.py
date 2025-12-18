import pygame
import sys
from settings import *
from sprites import Player
from managers import SpawnManager

class Game:
    def __init__(self):
        """Initialize the game window and systems."""
        pygame.init()
        # DOUBLEBUF helps with X11 forwarding smoothness
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # 1. Groups: Containers for sprites
        # 'all_sprites' is used for drawing everything in order
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # 2. Entities
        self.player = Player([self.all_sprites])
        
        # 3. Managers
        # We pass [self.all_sprites, self.enemies] so enemies are added to BOTH groups
        self.spawn_manager = SpawnManager(self.player, [self.all_sprites, self.enemies])

    def run(self):
        """The main game loop."""
        while self.running:
            # dt is delta time in seconds (e.g., 0.016 for 60fps)
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
        # Update all sprites (calls their .update(dt) method)
        self.all_sprites.update(self.dt)
        
        # Update managers
        self.spawn_manager.update(self.dt)

    def draw(self):
        """Render everything to the screen."""
        self.screen.fill(COLOR_BLACK)
        
        # Pygame's built-in group draw method
        self.all_sprites.draw(self.screen)
        
        # User Feedback: Draw the target position
        # We only draw it if the player is moving (distance > 5 pixels)
        if self.player.pos.distance_to(self.player.target_pos) > 5:
            target = self.player.target_pos
            # Draw an 'X' or cross
            pygame.draw.line(self.screen, COLOR_WHITE, (target.x - 5, target.y), (target.x + 5, target.y), 2)
            pygame.draw.line(self.screen, COLOR_WHITE, (target.x, target.y - 5), (target.x, target.y + 5), 2)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
