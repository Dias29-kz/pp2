import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

food_types = [
    {"weight": 1, "color": (255, 0, 0), "lifetime": 6},
    {"weight": 2, "color": (255, 255, 0), "lifetime": 5},
    {"weight": 3, "color": (255, 140, 0), "lifetime": 4},
]

food = None
score = 0


def spawn_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))
        if pos not in snake:
            f = random.choice(food_types)
            return {
                "pos": pos,
                "weight": f["weight"],
                "color": f["color"],
                "time": time.time(),
                "life": f["lifetime"]
            }


food = spawn_food()

running = True
while running:
    clock.tick(10)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                direction = "UP"
            if e.key == pygame.K_DOWN:
                direction = "DOWN"
            if e.key == pygame.K_LEFT:
                direction = "LEFT"
            if e.key == pygame.K_RIGHT:
                direction = "RIGHT"

    x, y = snake[0]

    if direction == "UP":
        y -= CELL
    if direction == "DOWN":
        y += CELL
    if direction == "LEFT":
        x -= CELL
    if direction == "RIGHT":
        x += CELL

    new_head = (x, y)
    snake.insert(0, new_head)

    if time.time() - food["time"] > food["life"]:
        food = spawn_food()

    if snake[0] == food["pos"]:
        score += food["weight"]
        food = spawn_food()
    else:
        snake.pop()

    screen.fill((0, 0, 0))

    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*s, CELL, CELL))

    pygame.draw.rect(screen, food["color"], (*food["pos"], CELL, CELL))

    pygame.display.update()

pygame.quit()