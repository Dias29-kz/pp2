import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
GRAY = (70, 70, 70)
YELLOW = (255, 215, 0)

# Walls (simple obstacles)
walls = [
    pygame.Rect(200, 200, 20, 120),
    pygame.Rect(380, 280, 20, 120),
    pygame.Rect(260, 100, 100, 20),
]


def draw_grid():
    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_walls():
    # Draw obstacle walls
    for wall in walls:
        pygame.draw.rect(screen, YELLOW, wall)


def get_random_food_position(snake):
    # Generate random food position so that:
    # 1) It is not on a wall
    # 2) It is not on the snake body
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        food_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        on_wall = any(food_rect.colliderect(wall) for wall in walls)
        on_snake = (x, y) in snake

        if not on_wall and not on_snake:
            return (x, y)


def game_over_screen(score, level):
    screen.fill(BLACK)

    game_over_text = font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    level_text = small_font.render(f"Level: {level}", True, WHITE)
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 220))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 270))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 310))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 370))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    # Initial snake position
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    next_direction = direction

    food = get_random_food_position(snake)

    score = 0
    level = 1
    foods_eaten = 0
    speed = 8

    running = True
    while running:
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Change snake direction with arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    next_direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    next_direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    next_direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    next_direction = (CELL_SIZE, 0)

        direction = next_direction

        # Calculate new head position
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Check if snake leaves playing area
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over_screen(score, level)
            main()
            return

        # Check wall collision
        snake_head_rect = pygame.Rect(new_head[0], new_head[1], CELL_SIZE, CELL_SIZE)
        for wall in walls:
            if snake_head_rect.colliderect(wall):
                game_over_screen(score, level)
                main()
                return

        # Check self collision
        if new_head in snake:
            game_over_screen(score, level)
            main()
            return

        # Move snake
        snake.insert(0, new_head)

        # Check if snake eats food
        if new_head == food:
            score += 10
            foods_eaten += 1
            food = get_random_food_position(snake)

            # Increase level every 4 foods
            if foods_eaten % 4 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        draw_walls()

        # Draw snake
        for i, segment in enumerate(snake):
            rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(screen, DARK_GREEN, rect)
            else:
                pygame.draw.rect(screen, GREEN, rect)

        # Draw food
        food_rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        # Draw score and level
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        level_text = small_font.render(f"Level: {level}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.flip()


if __name__ == "__main__":
    main()