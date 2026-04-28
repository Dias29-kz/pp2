import pygame, random

pygame.init()

CELL = 20
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Snake body
snake = [(100,100),(80,100),(60,100)]
direction = "RIGHT"

# Food types: weight + lifetime
food_types = [
    {"weight":1, "color":(255,0,0), "life":None},
    {"weight":2, "color":(255,255,0), "life":5000},
    {"weight":3, "color":(255,140,0), "life":3000}
]

def spawn_food():
    """Create random food not on snake"""
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))
        if pos not in snake:
            f = random.choice(food_types)
            return {"pos":pos, "type":f, "time":pygame.time.get_ticks()}

food = spawn_food()
score = 0

running = True
while running:
    clock.tick(10)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # Change direction
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP: direction="UP"
            if e.key == pygame.K_DOWN: direction="DOWN"
            if e.key == pygame.K_LEFT: direction="LEFT"
            if e.key == pygame.K_RIGHT: direction="RIGHT"

    x,y = snake[0]

    # Move snake
    if direction=="UP": y-=CELL
    if direction=="DOWN": y+=CELL
    if direction=="LEFT": x-=CELL
    if direction=="RIGHT": x+=CELL

    snake.insert(0,(x,y))

    # Food disappears after time
    if food["type"]["life"]:
        if pygame.time.get_ticks() - food["time"] > food["type"]["life"]:
            food = spawn_food()

    # Eat food → increase score
    if snake[0] == food["pos"]:
        score += food["type"]["weight"]
        food = spawn_food()
    else:
        snake.pop()

    # Draw
    screen.fill((0,0,0))

    for s in snake:
        pygame.draw.rect(screen,(0,255,0),(*s,CELL,CELL))

    pygame.draw.rect(screen, food["type"]["color"], (*food["pos"],CELL,CELL))

    pygame.display.update()

pygame.quit()