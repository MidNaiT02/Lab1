import pygame
import random

# Initialize Pygame
pygame.init()

# Game display size and grid setup
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Font for displaying score and level
font = pygame.font.SysFont("Arial", 24)

# Snake setup: list of grid positions
snake = [(5, 5)]
snake_dir = (1, 0)  # moving right

# Score, level, and speed control
score = 0
level = 1
speed = 10  # Initial speed (frames per second)

# Clock to control game speed
clock = pygame.time.Clock()

# Food properties
food = None
food_weight = 1  # Points food gives
food_timer = 0  # Countdown for food expiration

# Function to generate food in an empty cell with random weight and timer
def spawn_food():
    global food_weight, food_timer
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            food_weight = random.choice([1, 2, 3])  # Random points: 1, 2, or 3
            food_timer = random.randint(5, 10) * speed  # Timer based on game speed
            return pos

# First food spawn
food = spawn_food()

# Draw game elements
def draw():
    screen.fill(BLACK)

    # Draw snake segments
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw food
    if food:
        fx, fy = food
        pygame.draw.rect(screen, RED, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Game loop
running = True
while running:
    clock.tick(speed)  # Control the game speed

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for snake movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, 1):
        snake_dir = (0, -1)
    elif keys[pygame.K_DOWN] and snake_dir != (0, -1):
        snake_dir = (0, 1)
    elif keys[pygame.K_LEFT] and snake_dir != (1, 0):
        snake_dir = (-1, 0)
    elif keys[pygame.K_RIGHT] and snake_dir != (-1, 0):
        snake_dir = (1, 0)

    # Calculate new head position
    head_x, head_y = snake[0]
    new_head = (head_x + snake_dir[0], head_y + snake_dir[1])

    # Check for collision with self or borders
    if (new_head in snake or
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
        print("Game Over!")
        running = False

    # Add new head to snake
    snake.insert(0, new_head)

    # Check if food was eaten
    if food and new_head == food:
        score += food_weight  # Add food's weight to score
        
        # Level up every 5 points
        if score % 5 == 0:
            level += 1
            speed += 2  # Increase speed as level increases

        # Spawn new food
        food = spawn_food()
    else:
        # Remove the tail if no food eaten
        snake.pop()

    # Decrease food timer and remove food if time runs out
    if food:
        food_timer -= 1
        if food_timer <= 0:
            food = spawn_food()

    # Redraw everything
    draw()

# Exit Pygame
pygame.quit()
