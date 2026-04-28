import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# TSIS3 Racer
# Ready version with images and sounds

# ---------- WINDOW ----------
WIDTH = 500
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

clock = pygame.time.Clock()
FPS = 120

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# ---------- ROAD ----------
ROAD_LEFT = 120
ROAD_RIGHT = 380

lanes = [
    ROAD_LEFT + 40,
    (ROAD_LEFT + ROAD_RIGHT) // 2,
    ROAD_RIGHT - 40
]

# ---------- LEVELS ----------
levels = {
    "easy": {"road_speed": 220, "player_speed": 340, "enemy_min": 250, "enemy_max": 350},
    "medium": {"road_speed": 300, "player_speed": 420, "enemy_min": 350, "enemy_max": 500},
    "hard": {"road_speed": 380, "player_speed": 500, "enemy_min": 500, "enemy_max": 700}
}

level_names = ["easy", "medium", "hard"]
selected_level_index = 0
current_level = level_names[selected_level_index]

# ---------- MENU ----------
game_state = "menu"
menu_options = ["PLAY", "GARAGE", "EXIT"]
selected_menu_index = 0
garage_index = 0

# ---------- BEST SCORE ----------
best_score_file = os.path.join(BASE_DIR, "best_score.txt")

def load_best_score():
    # Load best score from text file
    if os.path.exists(best_score_file):
        try:
            with open(best_score_file, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_best_score(score):
    # Save new best score
    with open(best_score_file, "w") as f:
        f.write(str(score))

best_score = load_best_score()

# ---------- SOUNDS ----------
menu_music = os.path.join(SOUNDS_DIR, "menu.wav")
game_music = os.path.join(SOUNDS_DIR, "background.wav")

coin_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "coin.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "crash.wav"))

coin_sound.set_volume(0.7)
crash_sound.set_volume(0.8)
pygame.mixer.music.set_volume(0.35)

def play_menu_music():
    # Play menu music loop
    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

def play_game_music():
    # Play game music loop
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

# ---------- IMAGES ----------
road_img = pygame.image.load(os.path.join(IMAGES_DIR, "Road.jpg")).convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Player skins
player_skins = []
for skin_file in ["main_car.jpg", "NPC1.jpg", "NPC2.jpg", "NPC3.jpg"]:
    img = pygame.image.load(os.path.join(IMAGES_DIR, skin_file)).convert_alpha()
    img = pygame.transform.scale(img, (40, 70))
    player_skins.append(img)

# Enemy cars
npc_images = []
for i in range(1, 10):
    img = pygame.image.load(os.path.join(IMAGES_DIR, f"NPC{i}.jpg")).convert_alpha()
    img = pygame.transform.scale(img, (40, 70))
    npc_images.append(img)

# Coin images with different values
coin_images = {
    1: pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR, "1coin.jpg")).convert_alpha(), (25, 25)),
    3: pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR, "3coin.jpg")).convert_alpha(), (25, 25)),
    5: pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR, "5coin.jpg")).convert_alpha(), (25, 25)),
}

# ---------- COINS ----------
def get_random_coin():
    # Random coin value with chance
    roll = random.randint(1, 100)
    if roll <= 75:
        return 1
    elif roll <= 95:
        return 3
    return 5

def respawn_coin(state):
    # Put coin in safe random lane
    while True:
        new_x = random.choice(lanes) - 12
        new_y = random.randint(-300, -100)

        safe = True
        for e in state["enemies"]:
            if abs(e["y"] - new_y) < 80 and abs(e["x"] - new_x) < 20:
                safe = False
                break

        if safe:
            state["coin_x"] = new_x
            state["coin_y"] = new_y
            state["coin_value"] = get_random_coin()
            break

# ---------- ENEMIES ----------
def is_safe_position(x, y, enemies, min_dist=120):
    # Avoid enemy spawn too close
    for e in enemies:
        if abs(e["y"] - y) < min_dist and abs(e["x"] - x) < 10:
            return False
    return True

def create_enemy(level_name):
    # Create one enemy car
    level = levels[level_name]
    return {
        "img": random.choice(npc_images),
        "x": random.choice(lanes) - 20,
        "y": random.randint(-800, -100),
        "current_speed": 0,
        "max_speed": random.uniform(level["enemy_min"], level["enemy_max"]),
        "acceleration": random.uniform(1.5, 2.5)
    }

def reset_game(level_name):
    # Reset all game values
    enemies = []

    for _ in range(4):
        while True:
            e = create_enemy(level_name)
            if is_safe_position(e["x"], e["y"], enemies):
                enemies.append(e)
                break

    return {
        "player_x": lanes[1] - 20,
        "player_y": HEIGHT - 100,
        "enemies": enemies,
        "coin_value": get_random_coin(),
        "coin_x": random.choice(lanes) - 12,
        "coin_y": -200,
        "coin_speed": 5,
        "road_y1": 0.0,
        "road_y2": -HEIGHT,
        "coins": 0,
        "score": 0,
        "game_over": False,
        "level": level_name,
        "skin_index": garage_index,
        "speed": 0
    }

state = None

# ---------- FONTS ----------
font = pygame.font.SysFont("Arial", 22, bold=True)
big_font = pygame.font.SysFont("Arial", 62, bold=True)
menu_font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 19)

# ---------- COLORS ----------
C_ACCENT = (255, 70, 40)
C_ACCENT2 = (255, 190, 0)
C_TEXT = (230, 230, 230)
C_DIM = (120, 120, 130)
C_WHITE = (255, 255, 255)

LEVEL_COLORS = {
    "easy": (60, 220, 80),
    "medium": (255, 180, 0),
    "hard": (255, 50, 40)
}

# ---------- UI ----------
def draw_gradient_bg():
    # Draw simple menu background
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(8 + (18 - 8) * t)
        g = 8
        b = int(18 + (8 - 18) * t)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_center(text, y, font_obj, color):
    # Draw text in center
    surf = font_obj.render(text, True, color)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

def update_best_score():
    # Update best score if needed
    global best_score
    if state["score"] > best_score:
        best_score = state["score"]
        save_best_score(best_score)

# ---------- MAIN LOOP ----------
play_menu_music()
running = True

while running:
    dt = clock.tick(FPS) / 2000

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_UP:
                    selected_menu_index = (selected_menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_menu_index = (selected_menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_LEFT and menu_options[selected_menu_index] == "PLAY":
                    selected_level_index = (selected_level_index - 1) % len(level_names)
                    current_level = level_names[selected_level_index]
                elif event.key == pygame.K_RIGHT and menu_options[selected_menu_index] == "PLAY":
                    selected_level_index = (selected_level_index + 1) % len(level_names)
                    current_level = level_names[selected_level_index]
                elif event.key == pygame.K_RETURN:
                    selected = menu_options[selected_menu_index]
                    if selected == "PLAY":
                        state = reset_game(current_level)
                        game_state = "playing"
                        play_game_music()
                    elif selected == "GARAGE":
                        game_state = "garage"
                    elif selected == "EXIT":
                        running = False

            elif game_state == "garage":
                if event.key == pygame.K_LEFT:
                    garage_index = (garage_index - 1) % len(player_skins)
                elif event.key == pygame.K_RIGHT:
                    garage_index = (garage_index + 1) % len(player_skins)
                elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    game_state = "menu"

            elif game_state == "playing":
                if state["game_over"] and event.key == pygame.K_r:
                    state = reset_game(state["level"])
                    play_game_music()
                elif state["game_over"] and event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    state = None
                    play_menu_music()

    keys = pygame.key.get_pressed()

    # ---------- UPDATE GAME ----------
    if game_state == "playing" and not state["game_over"]:
        level = levels[state["level"]]

        player_speed = level["player_speed"]
        road_speed_base = level["road_speed"]

        # Gas and brake
        speed_multiplier = 1.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            speed_multiplier = 1.45
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            speed_multiplier = 0.55

        player_speed *= speed_multiplier
        road_speed_base *= speed_multiplier
        state["speed"] = int(road_speed_base)

        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            state["player_x"] -= player_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            state["player_x"] += player_speed * dt

        # Road border collision
        if state["player_x"] < ROAD_LEFT or state["player_x"] > ROAD_RIGHT - 40:
            crash_sound.play()
            pygame.mixer.music.stop()
            state["game_over"] = True
            update_best_score()

        # Road scrolling
        road_move = road_speed_base * dt
        state["road_y1"] += road_move
        state["road_y2"] += road_move

        if state["road_y1"] >= HEIGHT:
            state["road_y1"] = -HEIGHT
        if state["road_y2"] >= HEIGHT:
            state["road_y2"] = -HEIGHT

        # Enemy movement
        for enemy in state["enemies"]:
            target_speed = enemy["max_speed"] * speed_multiplier
            enemy["current_speed"] += (target_speed - enemy["current_speed"]) * enemy["acceleration"] * dt
            enemy["y"] += enemy["current_speed"] * dt

            if enemy["y"] > HEIGHT:
                while True:
                    new_enemy = create_enemy(state["level"])
                    if is_safe_position(new_enemy["x"], new_enemy["y"], state["enemies"]):
                        enemy.update(new_enemy)
                        state["score"] += 1
                        break

        # Coin movement
        state["coin_y"] += state["coin_speed"] * 60 * dt * speed_multiplier
        if state["coin_y"] > HEIGHT:
            respawn_coin(state)

        # Collisions
        player_rect = pygame.Rect(state["player_x"], state["player_y"], 40, 70)

        for enemy in state["enemies"]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 40, 70)
            if player_rect.colliderect(enemy_rect):
                crash_sound.play()
                pygame.mixer.music.stop()
                state["game_over"] = True
                update_best_score()

        coin_rect = pygame.Rect(state["coin_x"], state["coin_y"], 25, 25)
        if player_rect.colliderect(coin_rect):
            coin_sound.play()
            state["coins"] += state["coin_value"]
            respawn_coin(state)

    # ---------- DRAW ----------
    screen.fill((20, 20, 20))

    if game_state == "menu":
        draw_gradient_bg()
        draw_center("RACER", 35, big_font, C_ACCENT)

        for i, option in enumerate(menu_options):
            color = C_ACCENT2 if i == selected_menu_index else C_TEXT
            prefix = "> " if i == selected_menu_index else "  "
            draw_center(prefix + option, 240 + i * 65, menu_font, color)

        draw_center("Difficulty: " + current_level.upper(), 490, small_font, LEVEL_COLORS[current_level])
        draw_center("UP/DOWN menu | LEFT/RIGHT difficulty | ENTER select", 540, small_font, C_DIM)
        draw_center("Best score: " + str(best_score), 590, small_font, C_ACCENT2)

    elif game_state == "garage":
        draw_gradient_bg()
        draw_center("GARAGE", 35, big_font, C_ACCENT2)
        screen.blit(player_skins[garage_index], (WIDTH // 2 - 20, HEIGHT // 2 - 35))
        draw_center(f"Skin {garage_index + 1} / {len(player_skins)}", HEIGHT // 2 + 70, menu_font, C_ACCENT2)
        draw_center("LEFT/RIGHT change skin | ENTER/ESC back", 650, small_font, C_DIM)

    elif game_state == "playing":
        screen.blit(road_img, (0, int(state["road_y1"])))
        screen.blit(road_img, (0, int(state["road_y2"])))

        screen.blit(player_skins[state["skin_index"]], (state["player_x"], state["player_y"]))

        for enemy in state["enemies"]:
            screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

        screen.blit(coin_images[state["coin_value"]], (state["coin_x"], state["coin_y"]))

        # HUD
        hud = pygame.Surface((WIDTH, 70), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 130))
        screen.blit(hud, (0, 0))

        score_text = font.render(f"SCORE {state['score']}", True, C_WHITE)
        coins_text = font.render(f"COINS {state['coins']}", True, C_ACCENT2)
        speed_text = font.render(f"{state['speed']} km/h", True, C_DIM)

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (WIDTH - coins_text.get_width() - 10, 10))
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, 40))

        if state["game_over"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            draw_center("GAME OVER", HEIGHT // 2 - 90, big_font, C_ACCENT)
            draw_center(f"Score: {state['score']}", HEIGHT // 2 - 15, menu_font, C_ACCENT2)
            draw_center("R - Restart | ESC - Menu", HEIGHT // 2 + 55, small_font, C_TEXT)

    pygame.display.update()

pygame.quit()
sys.exit()
