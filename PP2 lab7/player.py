import pygame

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# Load album cover
album_cover = pygame.image.load("album.jpg")
album_cover = pygame.transform.scale(album_cover, (WIDTH, HEIGHT))

# List of songs (Provide the full path or ensure the songs are in the same directory)
songs = ["music/song1.mp3", "music/song2.mp3", "music/song3.mp3", "music/song4.mp3"]
if not songs:
    print("No songs found!")
    exit()

# Variables
current_song_index = 0
pygame.mixer.music.load(songs[current_song_index])

# Function to play music
def play_music():
    pygame.mixer.music.play()
    print(f"Playing: {songs[current_song_index]}")

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()
    print("Music stopped.")

# Function to play next song
def next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    pygame.mixer.music.load(songs[current_song_index])
    play_music()

# Function to play previous song
def prev_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    pygame.mixer.music.load(songs[current_song_index])
    play_music()

# Keyboard control loop
running = True
print("Music Player Controls: P - Play, S - Stop, N - Next, B - Previous, Q - Quit")
while running:
    screen.blit(album_cover, (0, 0))  # Display album cover
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_music()
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_n:
                next_song()
            elif event.key == pygame.K_b:
                prev_song()
            elif event.key == pygame.K_q:
                running = False

pygame.quit()