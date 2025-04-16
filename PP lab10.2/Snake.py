import pygame
import random
import psycopg2
from datetime import datetime

# ========== Database Connection ==========
def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="lab10.2",  # ✅ Your custom DB
        user="postgres",
        password="12345678"
    )

def ensure_user(username):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
    conn.commit()
    cur.close()
    conn.close()

def save_score(username, score, level):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_scores (username, score, level) VALUES (%s, %s, %s)",
                (username, score, level))
    conn.commit()
    cur.close()
    conn.close()

def show_all_scores():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, score, level, saved_at FROM user_scores ORDER BY saved_at DESC LIMIT 10")
    rows = cur.fetchall()
    print("\n=== Recent Scores ===")
    for row in rows:
        print(f"{row[0]} | Score: {row[1]} | Level: {row[2]} | {row[3].strftime('%Y-%m-%d %H:%M:%S')}")
    print("=====================\n")
    cur.close()
    conn.close()

# ========== Pygame Setup ==========
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
WHITE, GREEN, RED, BLACK, BLUE = (255,255,255), (0,255,0), (255,0,0), (0,0,0), (0,0,255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

def draw_start_button():
    screen.fill(BLACK)
    title = font.render("Welcome to Snake Game", True, WHITE)
    button_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 - 25, 150, 50)
    pygame.draw.rect(screen, BLUE, button_rect)
    start_text = font.render("Start Game", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 - 10))
    pygame.display.flip()
    return button_rect

def wait_for_start():
    button = draw_start_button()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    return

# ========== User Setup ==========
username = input("Enter your username: ")
ensure_user(username)

# Always start fresh
score = 0
level = 1
speed = 10

# ========== Game Start ==========
wait_for_start()

snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_dir = (1, 0)
food = None
food_weight = 1
food_timer = 0

def spawn_food():
    global food_weight, food_timer
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            food_weight = random.choice([1, 2, 3])
            food_timer = random.randint(5, 10) * speed
            return pos

food = spawn_food()

def draw():
    screen.fill(BLACK)
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if food:
        fx, fy = food
        pygame.draw.rect(screen, RED, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    info = font.render(f"User: {username} | Score: {score} | Level: {level}", True, WHITE)
    screen.blit(info, (10, 10))
    pygame.display.flip()

# ========== Game Loop ==========
running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(username, score, level)
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, 1):
        snake_dir = (0, -1)
    elif keys[pygame.K_DOWN] and snake_dir != (0, -1):
        snake_dir = (0, 1)
    elif keys[pygame.K_LEFT] and snake_dir != (1, 0):
        snake_dir = (-1, 0)
    elif keys[pygame.K_RIGHT] and snake_dir != (-1, 0):
        snake_dir = (1, 0)
    elif keys[pygame.K_p]:
        print("Paused. Saving...")
        save_score(username, score, level)
        pygame.time.wait(1000)
        continue
    elif keys[pygame.K_s]:
        show_all_scores()
        pygame.time.wait(1000)
        continue

    head_x, head_y = snake[0]
    new_head = (head_x + snake_dir[0], head_y + snake_dir[1])

    if (new_head in snake or
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
        print("Game Over!")
        save_score(username, score, level)
        running = False
        continue

    snake.insert(0, new_head)

    if food and new_head == food:
        score += food_weight
        if score % 5 == 0:
            level += 1
            speed += 2
        food = spawn_food()
    else:
        snake.pop()

    if food:
        food_timer -= 1
        if food_timer <= 0:
            food = spawn_food()

    draw()

pygame.quit()
