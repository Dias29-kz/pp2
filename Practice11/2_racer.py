import pygame, random, sys

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE, GRAY, BLUE, BLACK = (255,255,255),(60,60,60),(0,120,255),(0,0,0)
YELLOW, ORANGE, RED = (255,220,0),(255,140,0),(220,0,0)

# Player and enemy
player = pygame.Rect(225, 590, 50, 80)
enemy = pygame.Rect(random.randint(100, 350), -100, 50, 80)

player_speed = 6
enemy_speed = 5

# Coins with different weights (points)
coin_types = [
    {"weight": 1, "color": YELLOW},
    {"weight": 3, "color": ORANGE},
    {"weight": 5, "color": RED}
]

coins = []
score = 0

# Increase difficulty every N points
N = 10
next_speed = N


def spawn_coin():
    """Create random coin on road"""
    data = random.choice(coin_types)
    coins.append({
        "rect": pygame.Rect(random.randint(120, 350), -30, 25, 25),
        "weight": data["weight"],
        "color": data["color"]
    })


running = True
while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= player_speed
    if keys[pygame.K_RIGHT]: player.x += player_speed

    # Enemy movement
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = -100

    # Coins
    if random.randint(1, 60) == 1:
        spawn_coin()

    for coin in coins[:]:
        coin["rect"].y += 4

        # Collect coin → add score
        if player.colliderect(coin["rect"]):
            score += coin["weight"]
            coins.remove(coin)

    # Increase enemy speed (difficulty)
    if score >= next_speed:
        enemy_speed += 1
        next_speed += N

    # Draw
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, BLACK, enemy)

    for coin in coins:
        pygame.draw.ellipse(screen, coin["color"], coin["rect"])

    pygame.display.update()

pygame.quit()