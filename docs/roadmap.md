# Development Roadmap: Protocol Overdrive

This roadmap has been revised to include industry stats-standards for complex software development, including code quality tools, testing, and containerization best practices.

## Phase 0: Foundations & Quality Standards (NEW)
**Goal**: Set up a professional development environment that enforces code quality from day one.
*   **Version Control**: Initialize Git repository.
*   **Dependency Management**: Create `requirements.txt` with specific versions.
    *   Add `pygame-ce>=2.3.0`
    *   Add Dev tools: `pytest` (testing), `black` (formatting), `flake8` (linting), `mypy` (type checking).
*   **Configuration**: Create `pyproject.toml` or `setup.cfg` to configure:
    *   Line length (e.g., 88 for Black).
    *   Linter rules.
*   **Why?**: in complex software, consistent style and automatic error catching are vital to prevent technical debt.

## Phase 1: Project Structure & Basic Loop
**Goal**: Establish the file structure and a working "black screen" application.
*   **Directory Setup**: 
    ```
    /project_root
    ├── src/                 # Source code (better than root for complex projects)
    │   ├── __init__.py
    │   ├── main.py
    │   ├── settings.py
    ├── tests/               # Dedicated test folder
    ├── docs/                # Documentation
    ├── data/                # Runtime data
    └── Dockerfile
    ```
*   **Skeleton Code**: Write `main.py` entry point and `settings.py`.
*   **Docker Setup**: Create `Dockerfile` and `docker-compose.yml` early to ensure the environment is consistent.
*   **Deliverable**: A blank window running via Docker.

## Phase 2: Core Movement & Entities
**Goal**: Implement the "Click-to-Move" mechanic and the fundamental enemy chasing logic.
*   **Player Class**: `sprites.py`
    *   Input handling (store target vector).
    *   Movement logic (vector math).
*   **Enemy Class**: `sprites.py`
    *   Simple chasing AI.
    *   **Variant**: Create a `FastEnemy` subclass (High Speed, Low HP) to practice class inheritance.
*   **Spawn System**: `managers.py`
    *   Randomized spawning logic off-screen.
*   **Deliverable**: Blue square moves to click, red triangles chase it.

## Phase 3: Combat, Charge Math & UI
**Goal**: Implement the Auto-Pistol and the fractional "Charge" accumulation system.
*   **Projectile System**: Class for bullets.
*   **Math Logic (TESTABLE)**:
    *   This logic should be unit-tested. Create a test in `tests/test_mechanics.py` to verify `charge` accumulates correctly (e.g., `0.0 + 0.2 = 0.2`) before visual implementation.
*   **UI Implementation**: Health bar and segmented Charge bar.
*   **Deliverable**: Auto-shooting, charge bar filling up.

## Phase 4: Abilities, State Machine & Robot Form
**Goal**: The complex State Machine and Skill system.
*   **Cooldown Manager**: `abilities.py`
    *   Logic to track timestamps for multiple skills (Q, W, E, R).
*   **State Implementation**:
    *   Use the **State Pattern** (or checking a state enum) to handle Human vs Robot logic cleanly.
    *   Robot "Armor" logic.
*   **Transformation**: 'T' key trigger, sprite swap, data persistence (charge preserved).
*   **Deliverable**: Full combat capability, transformation mechanics working.

## Phase 5: Game Loop, Progression & Persistence
**Goal**: Turn the mechanic demo into a playable game loop.
*   **Wave Manager**: Progressive difficulty scaling.
    *   **State**: Implement `WAVE_ACTIVE` and `WAVE_WAITING` states.
    *   **Timer**: Add a cooldown (e.g., 3s) between waves.
*   **Data Persistence**:
    *   `managers.py` handles loading/saving `data/leaderboard.json`.
    *   **Docker Volume**: Ensure the `data/` folder is mounted as a volume so `leaderboard.json` survives container restarts.
*   **Game Over Screen**: Input name, save score (or skip and restart).

## Phase 6: Dockerization & Release (Revised)
**Goal**: Finalize production-ready container.
*   **Optimization**: Ensure the Docker image is small (using `-slim` variants).
*   **Volume Mapping**: 
    *   `docker run -v $(pwd)/data:/app/data ...`
    *   This ensures that when the user saves a high score, it writes to the actual host disk, not just inside the disposable container.
*   **Run Scripts**: Create `run_game.sh` or `run_game.bat` to encapsulate the complex Docker command (forwarding X11/Display).

## Phase 7: Final Polish & Verification (NEW)
**Goal**: Ensure software stability.
*   **Run Tests**: `pytest` passed.
*   **Linting**: `flake8` passed.
*   **Manual Playtest**: Verify game feel.

