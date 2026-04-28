"""
game.py — Core Snake gameplay loop.

Imported and driven by main.py; returns the final (score, level) tuple
so main.py can handle the Game Over screen and database save.
"""

import random
import pygame
import config
import settings as settings_module


# ═══════════════════════════════════════════════════════════════
#  UTILITY HELPERS
# ═══════════════════════════════════════════════════════════════

def _draw_cell(screen, pos, color):
    rect = pygame.Rect(pos[0] * config.CELL_SIZE, pos[1] * config.CELL_SIZE,
                       config.CELL_SIZE, config.CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def _draw_text(screen, text, font, color, x, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))


# ═══════════════════════════════════════════════════════════════
#  FOOD
# ═══════════════════════════════════════════════════════════════

def _generate_food(snake, existing_foods, powerup, obstacles):
    """
    Spawn a new food item at a free cell (not snake, food, power-up, or obstacle).
    Type is chosen by FOOD_WEIGHTS.
    """
    blocked = (
        set(snake)
        | {f["pos"] for f in existing_foods}
        | ({powerup["pos"]} if powerup else set())
        | obstacles
    )
    # Build pool of free inner cells
    free = [
        (x, y)
        for x in range(1, config.COLS - 1)
        for y in range(1, config.ROWS - 1)
        if (x, y) not in blocked
    ]
    if not free:
        return None

    pos       = random.choice(free)
    food_type = random.choices(config.FOOD_TYPES, weights=config.FOOD_WEIGHTS, k=1)[0]
    return {
        "pos":        pos,
        "color":      food_type["color"],
        "weight":     food_type["weight"],
        "lifetime":   food_type["lifetime"],
        "poison":     food_type["poison"],
        "label":      food_type["label"],
        "spawn_time": pygame.time.get_ticks(),
    }


def _is_expired(food):
    if food["lifetime"] is None:
        return False
    return pygame.time.get_ticks() - food["spawn_time"] >= food["lifetime"]


def _draw_food(screen, food):
    _draw_cell(screen, food["pos"], food["color"])
    # Shrinking border for expiring foods
    if food["lifetime"] is not None:
        elapsed  = pygame.time.get_ticks() - food["spawn_time"]
        ratio    = max(0.0, 1 - elapsed / food["lifetime"])
        x = food["pos"][0] * config.CELL_SIZE
        y = food["pos"][1] * config.CELL_SIZE
        bw = max(1, int(4 * ratio))
        pygame.draw.rect(screen, config.WHITE,
                         (x, y, config.CELL_SIZE, config.CELL_SIZE), bw)


# ═══════════════════════════════════════════════════════════════
#  POWER-UPS
# ═══════════════════════════════════════════════════════════════

def _spawn_powerup(snake, foods, obstacles):
    """Create a random power-up at a free cell, or None if no space."""
    blocked = (
        set(snake)
        | {f["pos"] for f in foods}
        | obstacles
    )
    free = [
        (x, y)
        for x in range(1, config.COLS - 1)
        for y in range(1, config.ROWS - 1)
        if (x, y) not in blocked
    ]
    if not free:
        return None
    pos  = random.choice(free)
    kind = random.choice(config.POWERUP_TYPES)
    return {
        "pos":        pos,
        "kind":       kind["kind"],
        "color":      kind["color"],
        "label":      kind["label"],
        "symbol":     kind["symbol"],
        "spawn_time": pygame.time.get_ticks(),
    }


def _draw_powerup(screen, pu, font_small):
    _draw_cell(screen, pu["pos"], pu["color"])
    # Pulsing ring
    elapsed = pygame.time.get_ticks() - pu["spawn_time"]
    ratio   = max(0.0, 1 - elapsed / config.POWERUP_FIELD_LIFE)
    x = pu["pos"][0] * config.CELL_SIZE
    y = pu["pos"][1] * config.CELL_SIZE
    bw = max(1, int(3 * ratio))
    pygame.draw.rect(screen, config.WHITE, (x, y, config.CELL_SIZE, config.CELL_SIZE), bw)


# ═══════════════════════════════════════════════════════════════
#  OBSTACLES
# ═══════════════════════════════════════════════════════════════

def _generate_obstacles(snake, foods, powerup, existing, count):
    """
    Add *count* new wall-block cells. Avoids snake area, foods, power-up,
    and existing blocks.  Uses a simple flood-fill guard to avoid trapping
    the snake head.
    """
    blocked = (
        set(snake)
        | {f["pos"] for f in foods}
        | ({powerup["pos"]} if powerup else set())
        | existing
        # Safety buffer around snake head
        | {
            (snake[0][0] + dx, snake[0][1] + dy)
            for dx in range(-3, 4)
            for dy in range(-3, 4)
        }
    )
    candidates = [
        (x, y)
        for x in range(1, config.COLS - 1)
        for y in range(1, config.ROWS - 1)
        if (x, y) not in blocked
    ]
    if not candidates:
        return set()
    chosen = set(random.sample(candidates, min(count, len(candidates))))
    return chosen


def _is_reachable(snake_head, obstacles):
    """
    BFS from snake_head; returns True if at least 10 free cells are reachable
    (a rough guard against complete entrapment).
    """
    walls = (
        obstacles
        | {(x, 0) for x in range(config.COLS)}
        | {(x, config.ROWS - 1) for x in range(config.COLS)}
        | {(0, y) for y in range(config.ROWS)}
        | {(config.COLS - 1, y) for y in range(config.ROWS)}
    )
    visited = {snake_head}
    queue   = [snake_head]
    while queue and len(visited) < 10:
        cx, cy = queue.pop(0)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nxt = (cx + dx, cy + dy)
            if nxt not in visited and nxt not in walls:
                visited.add(nxt)
                queue.append(nxt)
    return len(visited) >= 10


# ═══════════════════════════════════════════════════════════════
#  GRID OVERLAY
# ═══════════════════════════════════════════════════════════════

def _draw_grid(screen):
    for x in range(0, config.WIDTH, config.CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 50), (x, 0), (x, config.HEIGHT))
    for y in range(0, config.HEIGHT, config.CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 50), (0, y), (config.WIDTH, y))


# ═══════════════════════════════════════════════════════════════
#  HUD
# ═══════════════════════════════════════════════════════════════

def _draw_hud(screen, font_small, score, level, personal_best,
              active_effect, effect_end, shield_active):
    # Score / level / best
    _draw_text(screen, f"Score: {score}",   font_small, config.WHITE,  8,  6)
    _draw_text(screen, f"Level: {level}",   font_small, config.BLUE,   8, 26)
    _draw_text(screen, f"Best:  {personal_best}", font_small, config.UI_GOLD, 8, 46)

    # Food legend (right side)
    legend = [
        ("1pt",    config.FOOD_RED),
        ("2pt",    config.FOOD_ORANGE),
        ("3pt",    config.FOOD_PURPLE),
        ("poison", config.FOOD_POISON),
    ]
    rx = config.WIDTH - 85
    for i, (label, col) in enumerate(legend):
        _draw_text(screen, f"● {label}", font_small, col, rx, 6 + i * 18)

    # Active power-up effect indicator
    if active_effect and pygame.time.get_ticks() < effect_end:
        remaining = (effect_end - pygame.time.get_ticks()) / 1000
        symbols = {"speed": "⚡", "slow": "🐢", "shield": "🛡"}
        sym = symbols.get(active_effect, "?")
        col = config.PU_SPEED if active_effect == "speed" else (
              config.PU_SLOW  if active_effect == "slow"  else config.PU_SHIELD)
        _draw_text(screen, f"{sym} {remaining:.1f}s", font_small, col,
                   config.WIDTH // 2 - 30, 6)

    # Shield indicator (lasts until triggered)
    if shield_active:
        _draw_text(screen, "🛡 SHIELD", font_small, config.PU_SHIELD,
                   config.WIDTH // 2 - 35, 6)


# ═══════════════════════════════════════════════════════════════
#  MAIN GAME FUNCTION
# ═══════════════════════════════════════════════════════════════

def run_game(screen, clock, font, font_small, personal_best: int) -> tuple[int, int]:
    """
    Run one complete game session.
    Returns (final_score, level_reached).
    """
    cfg = settings_module.load()
    snake_color      = tuple(cfg.get("snake_color", [0, 200, 0]))
    snake_color_dark = tuple(max(0, c - 80) for c in snake_color)
    grid_overlay     = cfg.get("grid_overlay", False)

    # ── Initial state ──────────────────────────────────────────
    snake         = [(5, 5), (4, 5), (3, 5)]
    direction     = (1, 0)
    next_dir      = (1, 0)

    obstacles: set = set()
    foods     = []
    powerup   = None

    score         = 0
    level         = 1
    speed         = config.INITIAL_SPEED
    foods_eaten   = 0     # cumulative eaten count (drives level-up)

    # Power-up state
    active_effect = None    # "speed" | "slow" | "shield" | None
    effect_end    = 0
    shield_active = False

    # Timers
    last_bonus_spawn  = pygame.time.get_ticks()
    last_pu_spawn     = pygame.time.get_ticks()

    # Seed initial food
    foods.append(_generate_food(snake, [], None, obstacles))

    # ── Snake-move timer ───────────────────────────────────────
    move_event = pygame.USEREVENT + 1
    pygame.time.set_timer(move_event, 1000 // speed)

    running = True
    while running:
        dt = clock.tick(config.FPS)

        # ── Events ────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.set_timer(move_event, 0)
                return score, level

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != (0,  1): next_dir = (0, -1)
                if event.key == pygame.K_DOWN  and direction != (0, -1): next_dir = (0,  1)
                if event.key == pygame.K_LEFT  and direction != (1,  0): next_dir = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0): next_dir = (1,  0)
                if event.key == pygame.K_ESCAPE:
                    pygame.time.set_timer(move_event, 0)
                    return score, level

            # ── Move snake on timer ───────────────────────────
            if event.type == move_event:
                direction = next_dir

                hx, hy  = snake[0]
                dx, dy  = direction
                new_head = (hx + dx, hy + dy)

                # Wall collision
                hit_wall = not (1 <= new_head[0] < config.COLS - 1
                                and 1 <= new_head[1] < config.ROWS - 1)
                # Self collision
                hit_self = new_head in snake
                # Obstacle collision
                hit_obs  = new_head in obstacles

                collision = hit_wall or hit_self or hit_obs

                if collision:
                    if shield_active:
                        shield_active = False
                        active_effect = None
                        # Teleport head to opposite wall edge if wall hit
                        if hit_wall:
                            nx = new_head[0] % (config.COLS - 1)
                            ny = new_head[1] % (config.ROWS - 1)
                            new_head = (max(1, nx), max(1, ny))
                        else:
                            # Self / obstacle: just skip the move
                            continue
                    else:
                        pygame.time.set_timer(move_event, 0)
                        running = False
                        break

                snake.insert(0, new_head)

                # ── Food collision ─────────────────────────────
                eaten = next((f for f in foods if f["pos"] == new_head), None)
                if eaten:
                    if eaten["poison"]:
                        # Shorten snake
                        for _ in range(config.POISON_SHORTEN):
                            if len(snake) > 1:
                                snake.pop()
                        if len(snake) <= config.MIN_SNAKE_LENGTH:
                            pygame.time.set_timer(move_event, 0)
                            running = False
                            foods.remove(eaten)
                            break
                    else:
                        score       += eaten["weight"]
                        foods_eaten += 1
                        # Level up
                        new_level = foods_eaten // config.FOODS_PER_LEVEL + 1
                        if new_level > level:
                            level = new_level
                            speed = config.INITIAL_SPEED + (level - 1) * 2
                            pygame.time.set_timer(move_event, 1000 // speed)
                            # Add obstacles from level 3
                            if level >= config.OBSTACLES_START_LEVEL:
                                new_obs = _generate_obstacles(
                                    snake, foods, powerup, obstacles,
                                    config.OBSTACLES_PER_LEVEL
                                )
                                # Only add if snake can still move
                                candidate = obstacles | new_obs
                                if _is_reachable(snake[0], candidate):
                                    obstacles = candidate

                    foods.remove(eaten)
                    # Ensure at least one permanent food remains
                    if not any(f["lifetime"] is None and not f["poison"] for f in foods):
                        f = _generate_food(snake, foods, powerup, obstacles)
                        if f:
                            foods.append(f)
                else:
                    snake.pop()

                # ── Power-up collision ─────────────────────────
                if powerup and new_head == powerup["pos"]:
                    kind = powerup["kind"]
                    if kind == "shield":
                        shield_active = True
                        active_effect = "shield"
                        effect_end    = 0   # shield lasts until triggered
                    elif kind == "speed":
                        active_effect = "speed"
                        effect_end    = pygame.time.get_ticks() + config.POWERUP_EFFECT_DURATION
                        pygame.time.set_timer(move_event, max(50, 1000 // (speed + 4)))
                    elif kind == "slow":
                        active_effect = "slow"
                        effect_end    = pygame.time.get_ticks() + config.POWERUP_EFFECT_DURATION
                        pygame.time.set_timer(move_event, 1000 // max(2, speed - 3))
                    powerup = None

        # ── Expire power-up effect ────────────────────────────
        if active_effect in ("speed", "slow") and pygame.time.get_ticks() >= effect_end:
            active_effect = None
            pygame.time.set_timer(move_event, 1000 // speed)

        # ── Remove expired food ───────────────────────────────
        foods = [f for f in foods if not _is_expired(f)]
        if not any(f["lifetime"] is None and not f["poison"] for f in foods):
            f = _generate_food(snake, foods, powerup, obstacles)
            if f:
                foods.append(f)

        # ── Spawn bonus food ──────────────────────────────────
        now = pygame.time.get_ticks()
        if now - last_bonus_spawn >= config.BONUS_SPAWN_INTERVAL:
            f = _generate_food(snake, foods, powerup, obstacles)
            if f:
                foods.append(f)
            last_bonus_spawn = now

        # ── Spawn / expire power-up ───────────────────────────
        if powerup is None and now - last_pu_spawn >= 7000:
            powerup = _spawn_powerup(snake, foods, obstacles)
            last_pu_spawn = now
        if powerup and now - powerup["spawn_time"] >= config.POWERUP_FIELD_LIFE:
            powerup = None
            last_pu_spawn = now

        # ── Draw ──────────────────────────────────────────────
        if not running:
            break

        screen.fill(config.BLACK)

        if grid_overlay:
            _draw_grid(screen)

        # Walls
        for x in range(config.COLS):
            _draw_cell(screen, (x, 0),             config.GRAY)
            _draw_cell(screen, (x, config.ROWS-1), config.GRAY)
        for y in range(config.ROWS):
            _draw_cell(screen, (0, y),             config.GRAY)
            _draw_cell(screen, (config.COLS-1, y), config.GRAY)

        # Obstacles
        for obs in obstacles:
            _draw_cell(screen, obs, config.OBSTACLE_COLOR)
            # Cross mark
            ox = obs[0] * config.CELL_SIZE + config.CELL_SIZE // 2
            oy = obs[1] * config.CELL_SIZE + config.CELL_SIZE // 2
            half = config.CELL_SIZE // 2 - 2
            pygame.draw.line(screen, config.DARK_GRAY,
                             (ox - half, oy - half), (ox + half, oy + half), 2)
            pygame.draw.line(screen, config.DARK_GRAY,
                             (ox + half, oy - half), (ox - half, oy + half), 2)

        # Food
        for food in foods:
            _draw_food(screen, food)

        # Power-up
        if powerup:
            _draw_powerup(screen, powerup, font_small)

        # Snake body
        for part in snake[1:]:
            _draw_cell(screen, part, snake_color_dark)
        # Snake head (brighter)
        _draw_cell(screen, snake[0], snake_color)

        # Shield aura on head
        if shield_active:
            hx = snake[0][0] * config.CELL_SIZE - 2
            hy = snake[0][1] * config.CELL_SIZE - 2
            pygame.draw.rect(screen, config.PU_SHIELD,
                             (hx, hy, config.CELL_SIZE + 4, config.CELL_SIZE + 4), 2)

        _draw_hud(screen, font_small, score, level, personal_best,
                  active_effect, effect_end, shield_active)

        pygame.display.flip()

    return score, level