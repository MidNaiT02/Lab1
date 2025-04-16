import pygame
import sys
import random
import time
import psycopg2

# --------- Подключение к базе данных ---------
conn = psycopg2.connect(
    database="Snake_game",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# --------- Инициализация Pygame ---------
pygame.init()

# --------- Ввод имени пользователя ---------
username = input("Введите ваше имя пользователя: ")

# Поиск пользователя
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if user:
    user_id = user[0]
    print(f"🎮 Добро пожаловать обратно, {username}！Ваш ID пользователя: {user_id}")
    
    # Показываем последний результат игрока
    cur.execute(
        "SELECT score, level, saved_at FROM user_scores WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1",
        (user_id,)
    )
    last_data = cur.fetchone()
    if last_data:
        print(f"🧾 Ваш последний результат: Счёт={last_data[0]}, Уровень={last_data[1]}, Время={last_data[2]}")
    else:
        print("📭 Не найдено прошлых записей.")

else:
    # Новый пользователь
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    print(f"👤 Новый игрок создан: {username}, ID={user_id}")

# --------- Запрос уровня и инициализация ---------
cur.execute(
    "SELECT score, level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1",
    (user_id,)
)
last_record = cur.fetchone()
score = last_record[0] if last_record else 0
FPS = last_record[1] if last_record else 10

# --------- Настройки игры ---------
HEIGHT = 600
WIDTH = 600
grid_SIZE = 20
grid_WIDTH = WIDTH // grid_SIZE
grid_HEIGHT = HEIGHT // grid_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size()).convert()
myfont = pygame.font.SysFont("SimHei", 20)

# --------- Фон сетки ---------
def drawGrid(surface):
    for y in range(0, grid_HEIGHT):
        for x in range(0, grid_WIDTH):
            r = pygame.Rect((x * grid_SIZE, y * grid_SIZE), (grid_SIZE, grid_SIZE))
            color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
            pygame.draw.rect(surface, color, r)

# --------- Класс змеи ---------
class Snake:
    def __init__(self):  # Исправили название конструктора с _init_ на __init__
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
        self.dead = False  # Инициализация атрибута 'dead'

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        if self.dead:
            return
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x * grid_SIZE, cur[1] + y * grid_SIZE)

        if new[0] < 0 or new[0] >= WIDTH or new[1] < 0 or new[1] >= HEIGHT:
            self.dead = True
            return

        if new in self.positions[2:]:
            self.dead = True
            return

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.__init__()  # Сброс при вызове конструктора снова

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (grid_SIZE, grid_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

# --------- Класс пищи ---------
class Food:
    def __init__(self):  # Исправили название конструктора с _init_ на __init__
        self.color = (223, 163, 49)
        self.position = (0, 0)
        self.weight = 1
        self.spawn_time = 0
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_WIDTH - 1) * grid_SIZE,
                         random.randint(0, grid_HEIGHT - 1) * grid_SIZE)
        self.weight = random.randint(1, 3)
        self.spawn_time = time.time()

    def is_expired(self):
        return time.time() - self.spawn_time > 3

    def draw(self, surface):
        r = pygame.Rect(self.position, (grid_SIZE, grid_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

# --------- Начало игры ---------
snake = Snake()
food = Food()
death_count = 0

# --------- Главный цикл ---------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cur.close()
            conn.close()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.turn(RIGHT)

            # 🔴 Нажмите P для сохранения
            elif event.key == pygame.K_p:
                cur.execute(
                    "INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)",
                    (user_id, score, FPS)
                )
                conn.commit()
                print(f"💾 Ручное сохранение успешно: Счёт={score}, Уровень={FPS}")

    if snake.dead:
        death_count += 1
        surface.fill((255, 0, 0))
        screen.blit(surface, (0, 0))
        screen.blit(myfont.render("Игра окончена!", True, (0, 0, 0)), (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

        if death_count == 2:
            cur.execute(
                "INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)",
                (user_id, score, FPS)
            )
            conn.commit()
            print(f"🎮 Автосохранение завершено: {username}, Счёт={score}, Уровень={FPS}")
            pygame.quit()
            cur.close()
            conn.close()
            sys.exit()

        snake.reset()
        food.randomize_position()
        score = 0
        FPS = 10
        continue

    drawGrid(surface)
    snake.move()

    if snake.get_head_position() == food.position:
        snake.length += food.weight
        score += food.weight
        FPS += 1
        food.randomize_position()

    if food.is_expired():
        food.randomize_position()

    snake.draw(surface)
    food.draw(surface)
    screen.blit(surface, (0, 0))

    # Русский интерфейс
    screen.blit(myfont.render(f"Пользователь: {username}", True, (0, 0, 0)), (5, 10))
    screen.blit(myfont.render(f"Счёт: {score}", True, (0, 0, 0)), (5, 30))
    screen.blit(myfont.render(f"Уровень: {FPS}", True, (0, 0, 0)), (5, 50))
    screen.blit(myfont.render("P: Сохранить игру | Автосохранение после второй смерти", True, (0, 0, 0)), (5, 70))

    pygame.display.flip()
    clock.tick(FPS)
