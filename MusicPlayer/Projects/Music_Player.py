import pygame
import os
import random
import tkinter as tk
from mutagen.mp3 import MP3

# Initialize Pygame
pygame.init()

# Set the width and height of the window (adjust as needed)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Create the Pygame window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Music Player")

# Set the path to the directory containing your music files
MUSIC_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Store the list of music files
music_files = []

# Initialize the current music index
current_music_index = 0

# Initialize shuffle state
shuffle_on = False

# Font settings for song information and duration
font = pygame.font.Font(None, 24)
text_color = (255, 255, 255)
song_info_pos = (50, 400)
duration_bar_pos = (50, 450)
duration_bar_width = WINDOW_WIDTH - 100
duration_bar_height = 10

# Load button images
play_image = pygame.image.load("play.png")
pause_image = pygame.image.load("pause.png")
previous_image = pygame.image.load("previous.png")
next_image = pygame.image.load("next.png")
shuffle_on_image = pygame.image.load("shuffle_on.png")
shuffle_off_image = pygame.image.load("shuffle_off.png")
spotify_logo = pygame.image.load("spotify_logo.png")

# Scale button images to fit the window
button_width = 50
button_height = 50
play_image = pygame.transform.scale(play_image, (button_width, button_height))
pause_image = pygame.transform.scale(pause_image, (button_width, button_height))
previous_image = pygame.transform.scale(previous_image, (button_width, button_height))
next_image = pygame.transform.scale(next_image, (button_width, button_height))
shuffle_on_image = pygame.transform.scale(shuffle_on_image, (button_width, button_height))
shuffle_off_image = pygame.transform.scale(shuffle_off_image, (button_width, button_height))
spotify_logo = pygame.transform.scale(spotify_logo, (300, 300))

# Calculate button positions
play_pos = (WINDOW_WIDTH // 2 - button_width // 2, WINDOW_HEIGHT - button_height - 20)
previous_pos = (play_pos[0] - 100, play_pos[1])
next_pos = (play_pos[0] + 100, play_pos[1])
shuffle_pos = (next_pos[0] + 100, play_pos[1])  # Adjusted position of shuffle button

# Load music files from the directory
def load_music_files(directory):
    global music_files
    music_files.clear()
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                music_files.append(os.path.join(directory, file))

# Load the initial music files
load_music_files(MUSIC_DIRECTORY)

# Load the current music file
def load_current_music():
    pygame.mixer.music.load(music_files[current_music_index])
    pygame.mixer.music.play()

# Play the music
load_current_music()

# Function to play music based on user's click
def play_clicked_music(song_index):
    global current_music_index
    current_music_index = song_index
    load_current_music()

# Game loop
running = True
paused = False
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if play_pos[0] <= mouse_pos[0] <= play_pos[0] + button_width and \
                    play_pos[1] <= mouse_pos[1] <= play_pos[1] + button_height:
                # Toggle play/pause
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True

            elif previous_pos[0] <= mouse_pos[0] <= previous_pos[0] + button_width and \
                    previous_pos[1] <= mouse_pos[1] <= previous_pos[1] + button_height:
                # Play the previous music file
                if shuffle_on:
                    current_music_index = random.randint(0, len(music_files) - 1)
                else:
                    current_music_index = (current_music_index - 1) % len(music_files)
                load_current_music()

            elif next_pos[0] <= mouse_pos[0] <= next_pos[0] + button_width and \
                    next_pos[1] <= mouse_pos[1] <= next_pos[1] + button_height:
                # Play the next music file
                if shuffle_on:
                    current_music_index = random.randint(0, len(music_files) - 1)
                else:
                    current_music_index = (current_music_index + 1) % len(music_files)
                load_current_music()

            elif shuffle_pos[0] <= mouse_pos[0] <= shuffle_pos[0] + button_width and \
                    shuffle_pos[1] <= mouse_pos[1] <= shuffle_pos[1] + button_height:
                # Toggle shuffle
                shuffle_on = not shuffle_on

            # Handle mouse clicks on the playbar
            elif duration_bar_pos[0] <= mouse_pos[0] <= duration_bar_pos[0] + duration_bar_width and \
                    duration_bar_pos[1] <= mouse_pos[1] <= duration_bar_pos[1] + duration_bar_height:
                # Calculate the position where the user clicked on the playbar
                click_pos_x = mouse_pos[0] - duration_bar_pos[0]
                # Calculate the percentage of the playbar clicked
                click_percentage = click_pos_x / duration_bar_width
                # Calculate the new position in the music file based on the percentage clicked
                new_position = int(click_percentage * pygame.mixer.Sound(music_files[current_music_index]).get_length())
                # Set the new position in the music file
                pygame.mixer.music.play(start=new_position)

    # Get the current position of the music in seconds
    current_time = pygame.mixer.music.get_pos() / 1000

    # Get the duration of the current song using Mutagen
    audio = MP3(music_files[current_music_index])
    total_time = audio.info.length

    # Convert time from seconds to minutes and seconds
    current_time_minutes = int(current_time // 60)
    current_time_seconds = int(current_time % 60)
    total_time_minutes = int(total_time // 60)
    total_time_seconds = int(total_time % 60)

    # Render the song information and duration text
    song_info_text = f"Playing: {os.path.basename(music_files[current_music_index])}"
    duration_text = f"{current_time_minutes:02}:{current_time_seconds:02} / {total_time_minutes:02}:{total_time_seconds:02}"
    song_info_surface = font.render(song_info_text, True, text_color)
    duration_surface = font.render(duration_text, True, text_color)

    # Calculate the width of the duration bar
    duration_bar_width_filled = int(
        (current_time / total_time) * duration_bar_width
    )

    # Update the display
    window.fill((0, 0, 0))  # Fill the window with a dark background color
    window.blit(spotify_logo, (WINDOW_WIDTH // 2 - 150, 50))  # Adjust the position of the Spotify logo
    window.blit(previous_image, previous_pos)
    window.blit(play_image if not paused else pause_image, play_pos)
    window.blit(next_image, next_pos)
    window.blit(shuffle_on_image if shuffle_on else shuffle_off_image, shuffle_pos)
    window.blit(song_info_surface, song_info_pos)
    window.blit(duration_surface, (WINDOW_WIDTH - 150, 400))
    pygame.draw.rect(
        window,
        (255, 255, 255),
        pygame.Rect(duration_bar_pos[0], duration_bar_pos[1], duration_bar_width, duration_bar_height),
    )
    pygame.draw.rect(
        window,
        (0, 255, 0),
        pygame.Rect(
            duration_bar_pos[0],
            duration_bar_pos[1],
            duration_bar_width_filled,
            duration_bar_height,
        ),
    )

    # Handle mouse clicks on the song list
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] < song_info_pos[1]:
            clicked_index = mouse_pos[1] // 30  # Assuming each song entry has a height of 30 pixels
            if clicked_index < len(music_files):
                play_clicked_music(clicked_index)

    pygame.display.update()
