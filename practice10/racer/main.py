import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
YELLOW = (255, 255, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)

# Road settings
ROAD_LEFT = 50
ROAD_RIGHT = WIDTH - 50
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)

# Game settings
FPS = 60


class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 90
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_car(self.image, BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 6

    def draw_car(self, surface, color):
        # Main body
        pygame.draw.rect(surface, color, (5, 20, 40, 60), border_radius=8)
        # Roof
        pygame.draw.rect(surface, (180, 220, 255), (12, 5, 26, 25), border_radius=6)
        # Wheels
        pygame.draw.rect(surface, BLACK, (0, 20, 6, 18), border_radius=3)
        pygame.draw.rect(surface, BLACK, (44, 20, 6, 18), border_radius=3)
        pygame.draw.rect(surface, BLACK, (0, 62, 6, 18), border_radius=3)
        pygame.draw.rect(surface, BLACK, (44, 62, 6, 18), border_radius=3)

    def update(self, keys):
        # Move left
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # Move right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player inside the road
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 90
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_car(self.image, RED)
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = 5

    def draw_car(self, surface, color):
        pygame.draw.rect(surface, color, (5, 20, 40, 60), border_radius=8)
        pygame.draw.rect(surface, (240, 240, 255), (12, 5, 26, 25), border_radius=6)
        pygame.draw.rect(surface, BLACK, (0, 20, 6, 18), border_radius=3)
        pygame.draw.rect(surface, BLACK, (44, 20, 6, 18), border_radius=3)
        pygame.draw.rect(surface, BLACK, (0, 62, 6, 18), border_radius=3)
        pygame.draw.rect(surface, BLACK, (44, 62, 6, 18), border_radius=3)

    def reset_position(self):
        self.rect.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.width)
        self.rect.y = random.randint(-300, -100)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 12
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), self.radius)
        pygame.draw.circle(self.image, BLACK, (15, 15), self.radius, 2)
        self.rect = self.image.get_rect()
        self.speed = 4
        self.active = False
        self.spawn()

    def spawn(self):
        # Randomly place coin on the road
        self.rect.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 40)
        self.rect.y = random.randint(-500, -100)
        self.active = True

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            # Respawn coin again when it leaves the screen
            self.spawn()


def draw_road(lines_offset):
    # Fill background
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    # Draw side borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    # Draw middle dashed lines
    dash_height = 40
    dash_gap = 20
    x = WIDTH // 2 - 5
    y = -dash_height + lines_offset

    while y < HEIGHT:
        pygame.draw.rect(screen, WHITE, (x, y, 10, dash_height))
        y += dash_height + dash_gap


def game_over_screen(score, coins):
    screen.fill(BLACK)

    game_over_text = font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    coins_text = small_font.render(f"Coins: {coins}", True, WHITE)
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 260))
    screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, 300))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 360))

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
    player = PlayerCar()
    enemy = EnemyCar()
    coin = Coin()

    all_sprites = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    all_sprites.add(player, enemy, coin)
    enemy_group.add(enemy)
    coin_group.add(coin)

    road_line_offset = 0
    score = 0
    collected_coins = 0

    # Timer event to slowly increase difficulty
    INCREASE_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INCREASE_SPEED, 4000)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == INCREASE_SPEED:
                enemy.speed += 0.4
                coin.speed += 0.2

        keys = pygame.key.get_pressed()

        player.update(keys)
        enemy.update()
        coin.update()

        # Check collision with enemy
        if pygame.sprite.spritecollideany(player, enemy_group):
            game_over_screen(score, collected_coins)
            main()
            return

        # Check collision with coin
        if pygame.sprite.spritecollide(player, coin_group, False):
            collected_coins += 1
            score += 5
            coin.spawn()

        # Increase score over time
        score += 1

        # Animate road lines
        road_line_offset += 8
        if road_line_offset >= 60:
            road_line_offset = 0

        # Draw everything
        draw_road(road_line_offset)
        all_sprites.draw(screen)

        # Show score in top left
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Show collected coin count in top right
        coin_text = small_font.render(f"Coins: {collected_coins}", True, WHITE)
        screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()