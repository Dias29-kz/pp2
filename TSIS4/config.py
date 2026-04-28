# -------------------- DISPLAY --------------------
CELL_SIZE = 20
COLS      = 30
ROWS      = 20

WIDTH  = COLS * CELL_SIZE   # 600
HEIGHT = ROWS * CELL_SIZE   # 400

FPS = 60   # Pygame clock tick (not snake speed)

# -------------------- GAME TUNING --------------------
INITIAL_SPEED    = 7    # frames per second for snake movement
FOODS_PER_LEVEL  = 4    # food items eaten to reach next level
OBSTACLES_START_LEVEL = 3   # obstacles appear from this level onward
OBSTACLES_PER_LEVEL   = 3   # extra blocks added each level

BONUS_SPAWN_INTERVAL = 4000   # ms between bonus-food spawns
POWERUP_FIELD_LIFE   = 8000   # ms a power-up stays on the field
POWERUP_EFFECT_DURATION = 5000  # ms speed-boost / slow-motion effect lasts

POISON_SHORTEN = 2   # segments removed when snake eats poison food
MIN_SNAKE_LENGTH = 1 # if length drops to this after poison → game over

# -------------------- COLORS --------------------
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (100, 100, 100)
DARK_GRAY  = ( 40,  40,  40)
RED        = (220,   0,   0)
GREEN      = (  0, 200,   0)
DARK_GREEN = (  0, 120,   0)
BLUE       = ( 50, 150, 255)
YELLOW     = (255, 220,   0)

# Food colors
FOOD_RED    = (220,  50,  50)
FOOD_ORANGE = (255, 165,   0)
FOOD_PURPLE = (180,  80, 255)
FOOD_POISON = (120,   0,   0)   # dark red — poison

# Power-up colors
PU_SPEED  = (  0, 230, 230)   # cyan  — speed boost
PU_SLOW   = (255, 100, 200)   # pink  — slow motion
PU_SHIELD = (255, 215,   0)   # gold  — shield

# Obstacle color
OBSTACLE_COLOR = ( 80,  80,  80)

# UI palette
UI_BG        = ( 15,  15,  25)
UI_PANEL     = ( 25,  25,  45)
UI_BORDER    = ( 60,  60, 120)
UI_HIGHLIGHT = ( 80, 130, 255)
UI_TEXT      = (220, 220, 240)
UI_DIM       = (120, 120, 140)
UI_RED       = (220,  60,  60)
UI_GREEN     = ( 60, 200, 100)
UI_GOLD      = (255, 200,  50)

# -------------------- FOOD DEFINITIONS --------------------
FOOD_TYPES = [
    {
        "color":    FOOD_RED,
        "weight":   1,
        "lifetime": None,
        "poison":   False,
        "label":    "1pt",
    },
    {
        "color":    FOOD_ORANGE,
        "weight":   2,
        "lifetime": 5000,
        "poison":   False,
        "label":    "2pt",
    },
    {
        "color":    FOOD_PURPLE,
        "weight":   3,
        "lifetime": 3000,
        "poison":   False,
        "label":    "3pt",
    },
    {
        "color":    FOOD_POISON,
        "weight":   0,
        "lifetime": 6000,
        "poison":   True,
        "label":    "poison",
    },
]

# Spawn weights for each food type (red, orange, purple, poison)
FOOD_WEIGHTS = [55, 22, 13, 10]

# -------------------- POWER-UP DEFINITIONS --------------------
POWERUP_TYPES = [
    {"kind": "speed",  "color": PU_SPEED,  "label": "⚡ SPEED",  "symbol": "⚡"},
    {"kind": "slow",   "color": PU_SLOW,   "label": "🐢 SLOW",   "symbol": "🐢"},
    {"kind": "shield", "color": PU_SHIELD, "label": "🛡 SHIELD", "symbol": "🛡"},
]

# -------------------- DATABASE --------------------
DB_HOST     = "localhost"
DB_PORT     = 5432
DB_NAME     = "snake_game"
DB_USER     = "postgres"
DB_PASSWORD = "postgres"