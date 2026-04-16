import pygame


class MovingBallApp:
    def __init__(self):
        pygame.init()

        # Create the main game window
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Moving Ball Game")

        # Create a clock object to control the frame rate
        self.clock = pygame.time.Clock()

        # Define colors
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)

        # Ball settings
        self.radius = 25
        self.step = 20

        # Start the ball at the center of the screen
        self.x = self.width // 2
        self.y = self.height // 2

        # Create a font for on-screen text
        self.font = pygame.font.SysFont("Arial", 24)

    def move_up(self):
        # Move the ball up only if it stays inside the screen
        if self.y - self.step - self.radius >= 0:
            self.y -= self.step

    def move_down(self):
        # Move the ball down only if it stays inside the screen
        if self.y + self.step + self.radius <= self.height:
            self.y += self.step

    def move_left(self):
        # Move the ball left only if it stays inside the screen
        if self.x - self.step - self.radius >= 0:
            self.x -= self.step

    def move_right(self):
        # Move the ball right only if it stays inside the screen
        if self.x + self.step + self.radius <= self.width:
            self.x += self.step

    def draw(self):
        # Fill the background with white color
        self.screen.fill(self.white)

        # Draw instruction text
        instruction = self.font.render("Use arrow keys to move the red ball", True, self.black)
        self.screen.blit(instruction, (20, 20))

        # Show the current ball position
        position_text = self.font.render(f"Position: ({self.x}, {self.y})", True, self.black)
        self.screen.blit(position_text, (20, 55))

        # Draw the red ball
        pygame.draw.circle(self.screen, self.red, (self.x, self.y), self.radius)

    def run(self):
        running = True

        while running:
            # Process all events from the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # Move the ball when arrow keys are pressed
                    if event.key == pygame.K_UP:
                        self.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()

            # Draw all game elements
            self.draw()

            # Update the screen
            pygame.display.flip()

            # Limit the game to 60 frames per second
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = MovingBallApp()
    app.run()