import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Program")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
PURPLE = (150, 0, 150)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Canvas area
TOOLBAR_HEIGHT = 80
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Available colors
color_options = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE]

# Tools
TOOL_BRUSH = "brush"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"

current_tool = TOOL_BRUSH
current_color = BLACK
brush_size = 5

drawing = False
start_pos = None
last_pos = None


def draw_toolbar():
    # Draw toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Draw tool labels
    tools = [
        ("B: Brush", 20),
        ("R: Rectangle", 140),
        ("C: Circle", 310),
        ("E: Eraser", 440),
        ("+ / - Size", 560),
        ("X: Clear", 700),
    ]

    for text, x in tools:
        label = font.render(text, True, BLACK)
        screen.blit(label, (x, 10))

    # Show current tool
    current_tool_text = font.render(f"Current tool: {current_tool}", True, BLACK)
    screen.blit(current_tool_text, (20, 45))

    # Show brush size
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (240, 45))

    # Draw color selection boxes
    color_x = 400
    for color in color_options:
        pygame.draw.rect(screen, color, (color_x, 40, 30, 30))
        pygame.draw.rect(screen, BLACK, (color_x, 40, 30, 30), 2)
        color_x += 40


def draw_line_smooth(surface, color, start, end, width):
    # Draw smooth line by drawing circles between points
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        pygame.draw.circle(surface, color, start, width)
        return

    for i in range(distance + 1):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surface, color, (x, y), width)


def handle_color_click(pos):
    # Check if user clicked on one of the color boxes
    color_x = 400
    for color in color_options:
        rect = pygame.Rect(color_x, 40, 30, 30)
        if rect.collidepoint(pos):
            return color
        color_x += 40
    return None


def main():
    global drawing, start_pos, last_pos
    global current_tool, current_color, brush_size

    running = True
    while running:
        clock.tick(60)

        # Draw UI
        screen.fill(WHITE)
        draw_toolbar()
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Show preview shape while dragging
        if drawing and start_pos and current_tool in [TOOL_RECT, TOOL_CIRCLE]:
            mouse_pos = pygame.mouse.get_pos()
            preview_surface = canvas.copy()

            x1, y1 = start_pos
            x2, y2 = mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT

            if current_tool == TOOL_RECT:
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(preview_surface, current_color, rect, 2)

            elif current_tool == TOOL_CIRCLE:
                radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                pygame.draw.circle(preview_surface, current_color, (x1, y1), radius, 2)

            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard controls for tool selection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    current_tool = TOOL_BRUSH
                elif event.key == pygame.K_r:
                    current_tool = TOOL_RECT
                elif event.key == pygame.K_c:
                    current_tool = TOOL_CIRCLE
                elif event.key == pygame.K_e:
                    current_tool = TOOL_ERASER
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    brush_size += 1
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    if brush_size > 1:
                        brush_size -= 1
                elif event.key == pygame.K_x:
                    canvas.fill(WHITE)

            # Mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # If clicked on toolbar
                if mouse_pos[1] <= TOOLBAR_HEIGHT:
                    selected_color = handle_color_click(mouse_pos)
                    if selected_color is not None:
                        current_color = selected_color
                else:
                    drawing = True
                    start_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)
                    last_pos = start_pos

                    # For brush and eraser, start drawing immediately
                    if current_tool == TOOL_BRUSH:
                        pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                    elif current_tool == TOOL_ERASER:
                        pygame.draw.circle(canvas, WHITE, start_pos, brush_size)

            # Mouse movement while drawing
            if event.type == pygame.MOUSEMOTION and drawing:
                mouse_pos = pygame.mouse.get_pos()
                canvas_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                if current_tool == TOOL_BRUSH:
                    draw_line_smooth(canvas, current_color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

                elif current_tool == TOOL_ERASER:
                    draw_line_smooth(canvas, WHITE, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

            # Mouse button released
            if event.type == pygame.MOUSEBUTTONUP and drawing:
                mouse_pos = pygame.mouse.get_pos()
                end_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                if current_tool == TOOL_RECT:
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1]),
                    )
                    pygame.draw.rect(canvas, current_color, rect, 2)

                elif current_tool == TOOL_CIRCLE:
                    radius = int(math.sqrt(
                        (end_pos[0] - start_pos[0]) ** 2 +
                        (end_pos[1] - start_pos[1]) ** 2
                    ))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

                drawing = False
                start_pos = None
                last_pos = None


if __name__ == "__main__":
    main()