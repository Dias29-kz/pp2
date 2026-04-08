import os
import pygame


class MusicPlayerApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Create the main player window
        self.width = 900
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Music Player")

        # Create fonts for the interface
        self.title_font = pygame.font.SysFont("Arial", 34, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 22)

        # Define colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (40, 90, 180)
        self.green = (30, 160, 70)
        self.red = (190, 40, 40)

        # Create a clock object for FPS control
        self.clock = pygame.time.Clock()

        # Set the folder that contains audio files
        self.base_dir = os.path.dirname(__file__)
        self.music_dir = os.path.join(self.base_dir, "music", "sample_tracks")

        # Load all tracks from the folder
        self.playlist = self.load_tracks()
        self.current_index = 0

        # Player state
        self.is_playing = False

    def load_tracks(self):
        # Load all supported audio files from the sample_tracks folder
        supported_extensions = (".mp3", ".wav", ".ogg")
        tracks = []

        if os.path.exists(self.music_dir):
            for file_name in os.listdir(self.music_dir):
                if file_name.lower().endswith(supported_extensions):
                    full_path = os.path.join(self.music_dir, file_name)
                    tracks.append(full_path)

        # Sort tracks to keep playlist order stable
        tracks.sort()
        return tracks

    def get_current_track_name(self):
        # Return the current track name or a default message
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_index])

    def load_current_track(self):
        # Load the currently selected track into the mixer
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])

    def play_music(self):
        # Play the current track from the beginning
        if not self.playlist:
            return
        self.load_current_track()
        pygame.mixer.music.play()
        self.is_playing = True

    def stop_music(self):
        # Stop the current track
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        # Move to the next track and play it
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_music()

    def previous_track(self):
        # Move to the previous track and play it
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_music()

    def get_playback_position(self):
        # Get the current playback position in seconds
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0
        return pos_ms // 1000

    def draw_ui(self):
        # Fill the background
        self.screen.fill(self.white)

        # Draw title
        title = self.title_font.render("Music Player", True, self.black)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 30))

        # Draw current track label
        track_label = self.text_font.render("Current Track:", True, self.black)
        self.screen.blit(track_label, (80, 120))

        # Draw current track name
        track_name = self.text_font.render(self.get_current_track_name(), True, self.blue)
        self.screen.blit(track_name, (80, 160))

        # Draw playback status
        status_text = "Playing" if self.is_playing else "Stopped"
        status_color = self.green if self.is_playing else self.red
        status_render = self.text_font.render(f"Status: {status_text}", True, status_color)
        self.screen.blit(status_render, (80, 220))

        # Draw playback position
        position = self.get_playback_position()
        position_render = self.text_font.render(f"Position: {position} sec", True, self.black)
        self.screen.blit(position_render, (80, 280))

        # Draw playlist size
        playlist_render = self.text_font.render(f"Tracks in playlist: {len(self.playlist)}", True, self.black)
        self.screen.blit(playlist_render, (80, 340))

        # Draw keyboard controls
        controls_title = self.text_font.render("Keyboard Controls", True, self.black)
        self.screen.blit(controls_title, (560, 120))

        controls = [
            "P = Play",
            "S = Stop",
            "N = Next track",
            "B = Previous track",
            "Q = Quit"
        ]

        y = 170
        for item in controls:
            line = self.small_font.render(item, True, self.black)
            self.screen.blit(line, (560, y))
            y += 40

        # Draw a small help message
        note = self.small_font.render("Put .mp3, .wav or .ogg files into music/sample_tracks", True, self.black)
        self.screen.blit(note, (80, 430))

    def run(self):
        running = True

        while running:
            # Process all events from the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # Handle keyboard controls
                    if event.key == pygame.K_p:
                        self.play_music()
                    elif event.key == pygame.K_s:
                        self.stop_music()
                    elif event.key == pygame.K_n:
                        self.next_track()
                    elif event.key == pygame.K_b:
                        self.previous_track()
                    elif event.key == pygame.K_q:
                        running = False

            # Draw the interface
            self.draw_ui()

            # Update the screen
            pygame.display.flip()

            # Limit FPS
            self.clock.tick(30)

        pygame.mixer.music.stop()
        pygame.quit()