# Phase 1: The Foundation - How It Works

This document explains every file and design decision made during **Phase 1: Project Initialization**. This is the "Skeleton" of complex software.

---

## 1. Directory Structure: "Why so many folders?"

The first step in complex software is organization.

*   `src/` (Source): We keep our code here. **Why?** If you keep `main.py` in the root folder, it gets mixed up with `Dockerfile`, `README`, `.gitignore`, etc. As the project grows to 50+ files, putting code in `src/` keeps the root clean.
*   `data/`: For assets (images, sounds) and save files (`leaderboard.json`).
*   `tests/`: For automated code testing (we will add this later).
*   `docs/`: Where this file and the GDD live. **Why?** "Documentation is code." It should live with the project, not in Google Docs or random emails.

---

## 2. Docker Files: "The Container"

### `Dockerfile`
This is a recipe for baking a "Virtual Computer" that runs your game.

```dockerfile
# 1. Base Image
FROM python:3.11-slim
# WHY: We start with a minimal Linux installation that has Python 3.11 already installed.
# "slim" means it's smaller and faster than the full version.

# 2. System Dependencies
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    ...
# WHY: Pygame is a wrapper around a library called SDL (Simple DirectMedia Layer). 
# SDL needs C++ libraries to play sound and draw graphics. Linux doesn't have them by default.

# 3. Setup
WORKDIR /app
COPY requirements.txt .
RUN pip install ...
# WHY: We install libraries inside the container so they don't conflict with your Windows PC.

# 4. Command
CMD ["python", "src/main.py"]
# WHY: What to do when you turn the computer on.
```

### `docker-compose.yml`
This is a "Run Configuration" for the Dockerfile.

```yaml
services:
  game:
    build: .  # Build the Dockerfile in the current folder
    volumes:
      - .:/app
      # WHY: This is the "Magic Mirror". It maps your Windows folder (.) to the container's 
      # internal folder (/app). If you change main.py on Windows, it instantly changes 
      # inside Docker. You don't need to rebuild!
      
      - /tmp/.X11-unix:/tmp/.X11-unix
      # WHY: This allows the container to talk to your monitor (via VcXsrv).
    
    environment:
      - DISPLAY=host.docker.internal:0.0
      # WHY: Tells Linux "Screen 0 on the Windows Host is where you should draw pixels".
```

---

## 3. Python Code: "The Game Loop"

### `src/settings.py`
This file is just a list of variables.

*   **Rule**: **No Magic Numbers**.
*   **Bad**: `pygame.display.set_mode((1280, 720))`
*   **Good**: `pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`
*   **Why?** If you want to change resolution later, you change it in *one place*, not searching through 50 files.

### `src/main.py`
This implements the **Game Loop Pattern**, the heartbeat of every video game ever made.

```python
class Game:
    def __init__(self):
        # 1. Setup
        pygame.init() # Turn on the engine
        self.screen = ...
        self.clock = pygame.time.Clock() # Controls time

    def run(self):
        # The Infinite Loop
        while self.running:
            # A. INPUT
            self.handle_events() 
            # "Did the user press a key? Close the window?"
            
            # B. LOGIC
            self.update() 
            # "Move enemies 5 pixels forward." (Currently empty)
            
            # C. RENDER
            self.draw() 
            # "Paint the new state to the screen."
            
            self.dt = self.clock.tick(FPS) / 1000.0
            # WHY: This locks the loop to 60 FPS. 
            # dt (Delta Time) is how many seconds passed since the last frame (approx 0.016s).
            # We will use 'dt' for movement later so fast computers don't run the game faster.

if __name__ == "__main__":
    game = Game()
    game.run()
```
