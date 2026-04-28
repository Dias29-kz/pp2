import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Practice 11")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
RED = (220, 20, 60)

font = pygame.font.SysFont("Verdana", 20)

player = pygame.Rect(175, 500, 50, 80)
player_speed = 6

enemy = pygame.Rect(random.randint(50, 300), -100, 50, 80)
enemy_speed = 5

coins = []

coin_types = [
    {"weight": 1, "color": YELLOW},
    {"weight": 2, "color": ORANGE},
    {"weight": 3, "color": RED},
]

score = 0
timer = 0
N = 5
next_speed = N


def spawn_coin():
    data = random.choice(coin_types)
    coin = {
        "rect": pygame.Rect(random.randint(60, 320), -30, 25, 25),
        "weight": data["weight"],
        "color": data["color"]
    }
    coins.append(coin)


def reset_enemy():
    enemy.x = random.randint(60, 300)
    enemy.y = -100


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 40:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < 360:
        player.x += player_speed

    enemy.y += enemy_speed
    if enemy.top > HEIGHT:
        reset_enemy()

    timer += 1
    if timer >= FPS:
        spawn_coin()
        timer = 0

    for coin in coins[:]:
        coin["rect"].y += 4

        if coin["rect"].top > HEIGHT:
            coins.remove(coin)
        elif player.colliderect(coin["rect"]):
            score += coin["weight"]
            coins.remove(coin)

    if score >= next_speed:
        enemy_speed += 1
        next_speed += N

    if player.colliderect(enemy):
        print("Game Over:", score)
        running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, BLACK, enemy)

    for coin in coins:
        pygame.draw.ellipse(screen, coin["color"], coin["rect"])

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()