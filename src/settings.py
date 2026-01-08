"""
Configuration file for Protocol Overdrive.
Stores all constants to avoid magic numbers in the code.
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 45
TITLE = "Protocol Overdrive"

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_PLAYER = (50, 50, 255)  # Blue
COLOR_ENEMY = (255, 50, 50)   # Red

# Player settings
PLAYER_SPEED = 300  # Pixels per second
PLAYER_SIZE = 32
PLAYER_HP = 100
PROJECTILE_SPEED = 600
PROJECTILE_DAMAGE = 15
ATTACK_COOLDOWN = 0.5 # Seconds
ATTACK_RANGE = 350 # Pixels

# Charge settings
CHARGE_CAP = 8.0
CHARGE_PER_HIT = 0.20 # Float value!
