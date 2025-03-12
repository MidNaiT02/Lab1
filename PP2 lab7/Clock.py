import pygame
import time
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
CENTER = (WIDTH // 2, HEIGHT // 2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

# Load images
clock_face = pygame.image.load("mickeyclock.jpg")
clock_face = pygame.transform.scale(clock_face, (WIDTH, HEIGHT))
right_hand = pygame.image.load("right hand.png")
left_hand = pygame.image.load("left hand.png")

# Scale hands
right_hand = pygame.transform.scale(right_hand, (120, 40))  # Minute hand
left_hand = pygame.transform.scale(left_hand, (100, 35))  # Second hand

# Function to rotate hands around a fixed pivot
def rotate_hand(image, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect()
    rotated_rect.center = (
        pivot[0] + offset * math.cos(math.radians(-angle)),
        pivot[1] + offset * math.sin(math.radians(-angle))
    )
    return rotated_image, rotated_rect

# Clock loop
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(clock_face, (0, 0))
    
    # Get current time
    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    # Calculate angles
    minute_angle = -6 * minutes + 90
    second_angle = -6 * seconds + 90
    
    # Rotate hands while keeping the shoulder fixed
    right_hand_rotated, right_hand_rect = rotate_hand(right_hand, minute_angle, CENTER, 50)
    left_hand_rotated, left_hand_rect = rotate_hand(left_hand, second_angle, CENTER, 70)
    
    # Draw hands
    screen.blit(right_hand_rotated, right_hand_rect.topleft)
    screen.blit(left_hand_rotated, left_hand_rect.topleft)
    
    pygame.display.flip()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    time.sleep(1)  # Update every second

pygame.quit()