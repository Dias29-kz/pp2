"""
main.py — Screen manager and entry point for the Snake TSIS-4 project.

Screens implemented here:
  • username_entry_screen  — type a username before playing
  • main_menu_screen       — Play / Leaderboard / Settings / Quit
  • game_over_screen       — final score, level, personal best; Retry / Menu
  • leaderboard_screen     — Top-10 table fetched from PostgreSQL
  • settings_screen        — toggle grid, sound, pick snake colour

All rendering uses only Pygame.  No external UI library is required.
"""

import sys
import pygame
import config
import db
import settings as settings_module
from game import run_game


# ═══════════════════════════════════════════════════════════════
#  PYGAME SETUP
# ═══════════════════════════════════════════════════════════════

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("🐍  Snake — TSIS 4")
clock = pygame.time.Clock()

font_title  = pygame.font.SysFont("Arial", 38, bold=True)
font_large  = pygame.font.SysFont("Arial", 28, bold=True)
font        = pygame.font.SysFont("Arial", 22)
font_small  = pygame.font.SysFont("Arial", 18)
font_tiny   = pygame.font.SysFont("Arial", 14)


# ═══════════════════════════════════════════════════════════════
#  SHARED DRAWING HELPERS
# ═══════════════════════════════════════════════════════════════

def draw_text(text, fnt, color, x, y, center_x=False):
    surf = fnt.render(text, True, color)
    if center_x:
        x = x - surf.get_width() // 2
    screen.blit(surf, (x, y))


def draw_panel(rect, color=config.UI_PANEL, border=config.UI_BORDER, radius=8):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    pygame.draw.rect(screen, border, rect, 2, border_radius=radius)


class Button:
    """Simple rectangular button with hover highlight."""

    def __init__(self, text, x, y, w=160, h=38, fnt=None):
        self.text  = text
        self.rect  = pygame.Rect(x, y, w, h)
        self.fnt   = fnt or font
        self._hov  = False

    def draw(self, surf):
        col    = config.UI_HIGHLIGHT if self._hov else config.UI_PANEL
        border = config.WHITE        if self._hov else config.UI_BORDER
        pygame.draw.rect(surf, col,    self.rect, border_radius=6)
        pygame.draw.rect(surf, border, self.rect, 2, border_radius=6)
        ts = self.fnt.render(self.text, True, config.UI_TEXT)
        surf.blit(ts, ts.get_rect(center=self.rect.center))

    def update(self, mouse_pos):
        self._hov = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# ═══════════════════════════════════════════════════════════════
#  BACKGROUND (simple animated dots)
# ═══════════════════════════════════════════════════════════════

_dot_timer = 0

def draw_bg():
    global _dot_timer
    screen.fill(config.UI_BG)
    _dot_timer += 1
    for gx in range(0, config.WIDTH, 30):
        for gy in range(0, config.HEIGHT, 30):
            phase = (gx + gy + _dot_timer) % 60
            alpha = max(20, 40 - abs(phase - 30))
            pygame.draw.circle(screen, (alpha, alpha, alpha + 20), (gx, gy), 1)


# ═══════════════════════════════════════════════════════════════
#  USERNAME ENTRY SCREEN
# ═══════════════════════════════════════════════════════════════

def username_entry_screen() -> str:
    """
    Renders a text-input box for the player to type their username.
    Returns the entered username string.
    """
    username = ""
    cursor_visible = True
    cursor_timer   = 0
    MAX_LEN = 20

    btn_play = Button("▶  Play", config.WIDTH // 2 - 80, 270, 160, 40, font)

    while True:
        dt = clock.tick(config.FPS)
        cursor_timer += dt
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer   = 0

        mx, my = pygame.mouse.get_pos()
        btn_play.update((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    ch = event.unicode
                    if ch.isprintable() and len(username) < MAX_LEN:
                        username += ch

            if btn_play.is_clicked(event) and username.strip():
                return username.strip()

        # Draw
        draw_bg()

        draw_text("🐍  SNAKE",        font_title, config.UI_GREEN,
                  config.WIDTH // 2, 60, center_x=True)
        draw_text("Enter your username", font, config.UI_DIM,
                  config.WIDTH // 2, 130, center_x=True)

        # Input box
        box = pygame.Rect(config.WIDTH // 2 - 130, 165, 260, 44)
        draw_panel(box, config.UI_PANEL, config.UI_HIGHLIGHT if username else config.UI_BORDER)

        display_text = username + ("|" if cursor_visible else " ")
        ts = font_large.render(display_text, True, config.WHITE)
        screen.blit(ts, ts.get_rect(center=box.center))

        if not username:
            hint = font_small.render("type here …", True, config.UI_DIM)
            screen.blit(hint, hint.get_rect(center=box.center))

        btn_play.draw(screen)
        draw_text("Press Enter to confirm", font_tiny, config.UI_DIM,
                  config.WIDTH // 2, 320, center_x=True)

        pygame.display.flip()


# ═══════════════════════════════════════════════════════════════
#  MAIN MENU SCREEN
# ═══════════════════════════════════════════════════════════════

def main_menu_screen(username: str) -> str:
    """
    Returns one of: 'play', 'leaderboard', 'settings', 'quit'
    """
    bw, bh, bx = 180, 40, config.WIDTH // 2 - 90
    buttons = {
        "play":        Button("▶  Play",        bx, 160, bw, bh, font),
        "leaderboard": Button("🏆  Leaderboard", bx, 215, bw, bh, font),
        "settings":    Button("⚙  Settings",    bx, 270, bw, bh, font),
        "quit":        Button("✕  Quit",         bx, 325, bw, bh, font),
    }

    while True:
        clock.tick(config.FPS)
        mx, my = pygame.mouse.get_pos()
        for btn in buttons.values():
            btn.update((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            for key, btn in buttons.items():
                if btn.is_clicked(event):
                    return key

        draw_bg()
        draw_text("🐍  SNAKE",   font_title, config.UI_GREEN,
                  config.WIDTH // 2, 50, center_x=True)
        draw_text(f"Hello, {username}!", font_small, config.UI_DIM,
                  config.WIDTH // 2, 110, center_x=True)

        for btn in buttons.values():
            btn.draw(screen)

        draw_text("WASD / Arrow keys to move",
                  font_tiny, config.UI_DIM, config.WIDTH // 2, 378, center_x=True)

        pygame.display.flip()


# ═══════════════════════════════════════════════════════════════
#  GAME OVER SCREEN
# ═══════════════════════════════════════════════════════════════

def game_over_screen(score: int, level: int, personal_best: int) -> str:
    """
    Returns 'retry' or 'menu'.
    """
    bw, bh = 160, 40
    btn_retry = Button("↺  Retry",     config.WIDTH // 2 - 170, 300, bw, bh, font)
    btn_menu  = Button("⌂  Main Menu", config.WIDTH // 2 + 10,  300, bw, bh, font)

    is_new_best = score > personal_best

    while True:
        clock.tick(config.FPS)
        mx, my = pygame.mouse.get_pos()
        btn_retry.update((mx, my))
        btn_menu.update((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_retry.is_clicked(event):
                return "retry"
            if btn_menu.is_clicked(event):
                return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        draw_bg()

        # Panel
        panel = pygame.Rect(config.WIDTH // 2 - 175, 80, 350, 200)
        draw_panel(panel, config.UI_PANEL, config.UI_RED)

        draw_text("GAME  OVER", font_title, config.UI_RED,
                  config.WIDTH // 2, 100, center_x=True)

        draw_text(f"Score:  {score}",    font, config.WHITE,
                  config.WIDTH // 2, 155, center_x=True)
        draw_text(f"Level:  {level}",    font, config.BLUE,
                  config.WIDTH // 2, 183, center_x=True)

        best_label = f"Best:   {max(score, personal_best)}"
        best_color = config.UI_GOLD if is_new_best else config.UI_DIM
        draw_text(best_label, font, best_color,
                  config.WIDTH // 2, 211, center_x=True)

        if is_new_best:
            draw_text("★ New Personal Best! ★", font_small, config.UI_GOLD,
                      config.WIDTH // 2, 243, center_x=True)

        btn_retry.draw(screen)
        btn_menu.draw(screen)

        draw_text("R = Retry   |   Esc = Menu",
                  font_tiny, config.UI_DIM, config.WIDTH // 2, 352, center_x=True)

        pygame.display.flip()


# ═══════════════════════════════════════════════════════════════
#  LEADERBOARD SCREEN
# ═══════════════════════════════════════════════════════════════

def leaderboard_screen():
    """Fetch Top-10 from DB and display a ranked table."""
    rows    = db.get_leaderboard(10)
    btn_back = Button("← Back", config.WIDTH // 2 - 80, 360, 160, 36, font)

    while True:
        clock.tick(config.FPS)
        mx, my = pygame.mouse.get_pos()
        btn_back.update((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        draw_bg()

        draw_text("🏆  LEADERBOARD", font_title, config.UI_GOLD,
                  config.WIDTH // 2, 18, center_x=True)

        # Table header
        hx = 40
        hy = 68
        draw_text("#",        font_small, config.UI_DIM, hx,       hy)
        draw_text("Username", font_small, config.UI_DIM, hx + 35,  hy)
        draw_text("Score",    font_small, config.UI_DIM, hx + 195, hy)
        draw_text("Level",    font_small, config.UI_DIM, hx + 265, hy)
        draw_text("Date",     font_small, config.UI_DIM, hx + 330, hy)

        pygame.draw.line(screen, config.UI_BORDER, (40, hy + 20), (560, hy + 20), 1)

        if not rows:
            draw_text("No scores yet — be the first!", font, config.UI_DIM,
                      config.WIDTH // 2, 180, center_x=True)
        else:
            for i, row in enumerate(rows):
                ry  = 98 + i * 24
                col = config.UI_GOLD if i == 0 else (
                      (200, 200, 200) if i == 1 else (
                      (180, 120,  60) if i == 2 else config.UI_TEXT))

                rank_str = str(row.get("rank", i + 1))
                uname    = str(row.get("username", "?"))[:16]
                score_s  = str(row.get("score", 0))
                level_s  = str(row.get("level_reached", 1))
                played   = row.get("played_at")
                date_s   = played.strftime("%Y-%m-%d") if played else "—"

                draw_text(rank_str, font_small, col, hx,       ry)
                draw_text(uname,   font_small, col, hx + 35,  ry)
                draw_text(score_s, font_small, col, hx + 195, ry)
                draw_text(level_s, font_small, col, hx + 265, ry)
                draw_text(date_s,  font_tiny,  col, hx + 330, ry)

        btn_back.draw(screen)
        pygame.display.flip()


# ═══════════════════════════════════════════════════════════════
#  SETTINGS SCREEN
# ═══════════════════════════════════════════════════════════════

# Pre-defined snake colour choices
COLOUR_OPTIONS = [
    ("Green",  (0,   200,   0)),
    ("Cyan",   (0,   220, 220)),
    ("Yellow", (230, 220,   0)),
    ("Orange", (255, 140,   0)),
    ("Pink",   (255,  80, 180)),
    ("White",  (230, 230, 230)),
]


def settings_screen():
    """Toggle grid, sound, and snake colour; saves to settings.json."""
    cfg = settings_module.load()
    grid_on    = cfg.get("grid_overlay", False)
    sound_on   = cfg.get("sound",        True)
    sel_color  = tuple(cfg.get("snake_color", [0, 200, 0]))

    # Find index of current colour (default to 0)
    col_idx = 0
    for i, (_, c) in enumerate(COLOUR_OPTIONS):
        if tuple(c) == sel_color:
            col_idx = i
            break

    # Buttons
    btn_grid  = Button("", config.WIDTH // 2 + 30, 140, 90, 32, font_small)
    btn_sound = Button("", config.WIDTH // 2 + 30, 190, 90, 32, font_small)
    btn_prev  = Button("◀", config.WIDTH // 2 - 20, 250, 34, 32, font_small)
    btn_next  = Button("▶", config.WIDTH // 2 + 90, 250, 34, 32, font_small)
    btn_save  = Button("💾 Save & Back", config.WIDTH // 2 - 90, 320, 180, 40, font)

    def _label(flag):
        return "ON" if flag else "OFF"

    while True:
        clock.tick(config.FPS)
        mx, my = pygame.mouse.get_pos()
        for b in [btn_grid, btn_sound, btn_prev, btn_next, btn_save]:
            b.update((mx, my))

        # Update button labels dynamically
        btn_grid.text  = _label(grid_on)
        btn_sound.text = _label(sound_on)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if btn_grid.is_clicked(event):
                grid_on = not grid_on
            if btn_sound.is_clicked(event):
                sound_on = not sound_on
            if btn_prev.is_clicked(event):
                col_idx = (col_idx - 1) % len(COLOUR_OPTIONS)
            if btn_next.is_clicked(event):
                col_idx = (col_idx + 1) % len(COLOUR_OPTIONS)
            if btn_save.is_clicked(event):
                cfg["grid_overlay"] = grid_on
                cfg["sound"]        = sound_on
                cfg["snake_color"]  = list(COLOUR_OPTIONS[col_idx][1])
                settings_module.save(cfg)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        draw_bg()
        draw_text("⚙  SETTINGS", font_title, config.UI_TEXT,
                  config.WIDTH // 2, 50, center_x=True)

        # Grid row
        draw_text("Grid overlay:", font, config.UI_TEXT,
                  config.WIDTH // 2 - 130, 148)
        btn_grid.draw(screen)

        # Sound row
        draw_text("Sound:",        font, config.UI_TEXT,
                  config.WIDTH // 2 - 130, 198)
        btn_sound.draw(screen)

        # Snake colour row
        draw_text("Snake colour:", font, config.UI_TEXT,
                  config.WIDTH // 2 - 130, 258)
        btn_prev.draw(screen)
        # Colour swatch
        swatch_name, swatch_col = COLOUR_OPTIONS[col_idx]
        sw_rect = pygame.Rect(config.WIDTH // 2 + 28, 253, 58, 32)
        pygame.draw.rect(screen, swatch_col, sw_rect, border_radius=4)
        pygame.draw.rect(screen, config.UI_BORDER, sw_rect, 1, border_radius=4)
        draw_text(swatch_name, font_tiny, config.BLACK if sum(swatch_col) > 400 else config.WHITE,
                  sw_rect.centerx - 18, sw_rect.y + 9)
        btn_next.draw(screen)

        btn_save.draw(screen)

        pygame.display.flip()


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    # Initialise database schema (no-op if DB unreachable)
    db.init_db()

    # 1. Get username
    username  = username_entry_screen()
    player_id = db.get_or_create_player(username)

    while True:
        # 2. Main menu
        choice = main_menu_screen(username)

        if choice == "quit":
            break

        elif choice == "leaderboard":
            leaderboard_screen()

        elif choice == "settings":
            settings_screen()

        elif choice == "play":
            action = "retry"
            while action == "retry":
                personal_best = db.get_personal_best(player_id) if player_id else 0
                score, level  = run_game(screen, clock, font, font_small, personal_best)

                # Save to DB
                if player_id is not None:
                    db.save_session(player_id, score, level)
                    personal_best = db.get_personal_best(player_id)

                action = game_over_screen(score, level, personal_best)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()