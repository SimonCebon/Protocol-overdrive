import pygame
import sys
from settings import *

class Game:
    def __init__(self):
        """Initialize the game window and systems."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """The main game loop."""
        while self.running:
            # 1. Handle Input
            self.handle_events()
            
            # 2. Update Game Logic
            self.update()
            
            # 3. Draw to Screen
            self.draw()
            
            # Cap the frame rate
            self.dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

    def handle_events(self):
        """Process keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def update(self):
        """Update game state."""
        pass

    def draw(self):
        """Render everything to the screen."""
        self.screen.fill(COLOR_BLACK)
        
        # TODO: Draw sprites here
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
