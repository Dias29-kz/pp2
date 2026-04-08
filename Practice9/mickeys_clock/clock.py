import os
import math
import datetime
import pygame


class MickeyClockApp:
    def __init__(self):
        pygame.init()

        # Create the clock window
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mickey's Clock")

        # Create a clock object to control frame rate
        self.fps_clock = pygame.time.Clock()

        # Set the center of the clock
        self.center = (self.width // 2, self.height // 2)

        # Define colors
        self.bg_color = (245, 245, 245)
        self.black = (0, 0, 0)
        self.red = (220, 30, 30)
        self.blue = (50, 90, 200)

        # Create fonts for text
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)

        # Build the path to the Mickey hand image
        self.base_dir = os.path.dirname(__file__)
        self.image_path = os.path.join(self.base_dir, "images", "mickey_hand.png")

        # Try to load the hand image
        self.hand_image = self.load_hand_image()

        # Set lengths for both hands
        self.minute_hand_length = 180
        self.second_hand_length = 220

    def load_hand_image(self):
        # Load the hand image if it exists, otherwise return None
        if os.path.exists(self.image_path):
            image = pygame.image.load(self.image_path).convert_alpha()
            return image
        return None

    def get_hand_angle(self, value, max_value):
        # Convert a time value into a rotation angle
        return (value / max_value) * 360

    def draw_clock_face(self):
        # Draw the main clock circle
        pygame.draw.circle(self.screen, self.black, self.center, 250, 4)
        pygame.draw.circle(self.screen, self.black, self.center, 12)

        # Draw title text
        title = self.font.render("Mickey's Clock", True, self.black)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 30))

        # Draw helper text
        info = self.small_font.render("Right hand = minutes | Left hand = seconds", True, self.black)
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 70))

        # Draw minute markers around the clock
        for i in range(60):
            angle_deg = i * 6
            angle_rad = math.radians(angle_deg - 90)

            outer_x = self.center[0] + math.cos(angle_rad) * 235
            outer_y = self.center[1] + math.sin(angle_rad) * 235

            if i % 5 == 0:
                inner_length = 210
                thickness = 4
            else:
                inner_length = 222
                thickness = 2

            inner_x = self.center[0] + math.cos(angle_rad) * inner_length
            inner_y = self.center[1] + math.sin(angle_rad) * inner_length

            pygame.draw.line(
                self.screen,
                self.black,
                (inner_x, inner_y),
                (outer_x, outer_y),
                thickness
            )

    def draw_fallback_hand(self, angle, length, color, width):
        # Draw a simple line hand if the image file is missing
        angle_rad = math.radians(angle - 90)

        end_x = self.center[0] + math.cos(angle_rad) * length
        end_y = self.center[1] + math.sin(angle_rad) * length

        pygame.draw.line(self.screen, color, self.center, (end_x, end_y), width)
        pygame.draw.circle(self.screen, self.black, self.center, 10)

    def draw_rotated_hand_image(self, angle, length, flip_x=False):
        # Resize the image to match the required hand length
        scaled = pygame.transform.smoothscale(self.hand_image, (60, length))

        # Flip one hand to make left and right hands look different
        if flip_x:
            scaled = pygame.transform.flip(scaled, True, False)

        # Rotate the hand image
        rotated = pygame.transform.rotate(scaled, -angle)

        # Place the rotated image near the center of the clock
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def draw_hands(self, minutes, seconds):
        # Calculate angles for minute and second hands
        minute_angle = self.get_hand_angle(minutes, 60)
        second_angle = self.get_hand_angle(seconds, 60)

        if self.hand_image:
            # Draw the minute hand using the image
            self.draw_rotated_hand_image(minute_angle, self.minute_hand_length, flip_x=False)

            # Draw the second hand using the image
            self.draw_rotated_hand_image(second_angle, self.second_hand_length, flip_x=True)
        else:
            # Use simple line hands if the image is missing
            self.draw_fallback_hand(minute_angle, self.minute_hand_length, self.blue, 8)
            self.draw_fallback_hand(second_angle, self.second_hand_length, self.red, 4)

    def draw_time_text(self, minutes, seconds):
        # Display current time using only minutes and seconds
        time_text = f"{minutes:02d}:{seconds:02d}"
        rendered = self.font.render(time_text, True, self.black)
        self.screen.blit(
            rendered,
            (self.width // 2 - rendered.get_width() // 2, self.height - 80)
        )

    def run(self):
        running = True

        while running:
            # Process all events from the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get the current system time
            now = datetime.datetime.now()
            minutes = now.minute
            seconds = now.second

            # Fill the background
            self.screen.fill(self.bg_color)

            # Draw all clock elements
            self.draw_clock_face()
            self.draw_hands(minutes, seconds)
            self.draw_time_text(minutes, seconds)

            # Update the screen
            pygame.display.flip()

            # Limit FPS while keeping the animation smooth
            self.fps_clock.tick(30)

        pygame.quit()