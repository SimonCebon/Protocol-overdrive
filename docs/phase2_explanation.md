# Phase 2: Core Movement & Enemy "Horde" - Code Explanation

We have now implemented the "Muscles" of the game: Input, Movement, and Spawning.

### 1. Sprite inheritance (`src/sprites.py`)
This is a classic Object-Oriented pattern.

```python
class Entity(pygame.sprite.Sprite):
    ...
class Player(Entity):
    ...
class Enemy(Entity):
    ...
class FastEnemy(Enemy):
    ...
```

*   **Why use Inheritance?**
    *   `Entity` holds the code that *everyone* needs (`self.pos`, `self.rect`, `self.image`). We write this ONCE.
    *   `Player` adds input logic.
    *   `Enemy` adds chasing logic.
    *   `FastEnemy` changes just the *parameters* (speed, color) but reuses the *logic* from `Enemy`.
*   **Vector Math**:
    *   `direction = target - current` gives you a vector pointing to the target.
    *   `.normalize()` forces that vector to have a length of 1 (unit vector). This ensures diagonal movement isn't faster than straight movement.

### 2. The Spawning Logic (`src/managers.py`)
We kept this logic OUT of `main.py`.

*   **Single Responsibility Principle**: `main.py` should only handle the high-level loop. It shouldn't care about "how to calculate random coordinates".
*   **The Timer**:
    *   `self.spawn_timer += dt * 1000`. We count up in milliseconds.
    *   When we hit `interval` (2000ms), we spawn and reset.

### 3. Sprite Groups (`src/main.py`)
Pygame helps us manage hundreds of objects using **Groups**.

```python
self.all_sprites = pygame.sprite.Group()
self.enemies = pygame.sprite.Group()
```

*   **Efficiency**: Instead of looping `for sprite in list: sprite.draw()`, we just call `all_sprites.draw(screen)`.
*   **Logic Separation**:
    *   `all_sprites`: Used to Draw everything.
    *   `enemies`: Used later to check collisions (Bullet vs Enemy).
