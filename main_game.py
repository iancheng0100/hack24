import random

import pygame
import numpy as np
import time
from datetime import timedelta

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 50
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
HEAD = (0, 255, 0)
FOOD = (255, 0, 0)
BODY = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 200), (x, 800))
    for y in range(200, HEIGHT+200, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
    pygame.draw.line(screen, GRAY, (600, 200), (600, 800))

def draw_cells(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = (0,0,0)
            if grid[row, col] == 1:
                color = WHITE
            elif grid[row, col] == 2:
                color = HEAD
            elif grid[row, col] == 3:
                color = BODY
            elif grid[row, col] == 4:
                color = FOOD

            pygame.draw.rect(
                screen,
                color,
                (col * CELL_SIZE, row * CELL_SIZE+200, CELL_SIZE, CELL_SIZE)
            )


# Label function
def draw_time_label(screen, time_float):
    # Format the time as "s.ms"
    time_text = f"{time_float:.3f} s"

    # Render the text
    text_surface = pygame.font.Font(None, 50).render(time_text, True, WHITE)

    # Get the rectangle of the text
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))

    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)

def draw_score_label(screen, score):
    # Format the time as "s.ms"
    time_text = f"Score: {score}"

    # Render the text
    text_surface = pygame.font.Font(None, 30).render(time_text, True, WHITE)

    # Get the rectangle of the text
    text_rect = text_surface.get_rect(center=(500, 120))

    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)

def update_grid_conway(grid):
    new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Count live neighbors
            neighbors = np.count_nonzero(grid[row - 1 : row + 2, col - 1 : col + 2] == 1)
            if grid[row, col] == 1:
                neighbors -= 1
            # Apply Conway's rules
            if grid[row, col] == 1:
                if 4 > neighbors > 1:
                    new_grid[row, col] = 1
            else:
                if neighbors == 3:
                    new_grid[row, col] = 1
    return new_grid

def update_grid_snake(grid, snake):
    grid[snake[0]] = 2
    for seg in snake[1:]:
        grid[seg] = 3

def update_grid_food(grid, food):
    grid[food] = 4

def update_grid_foods(grid, foods):
    for food in foods:
        update_grid_food(grid, food)

def move_snake(snake, direction):
    return [(snake[0][0] + direction[0], snake[0][1] + direction[1])] + snake

def is_food(grid, new_head):
    if grid[new_head] == 4:
        return True
    return False

def check_collision(snake):
    head = snake[0]
    # Check wall collision
    if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
        return True
    # Check self collision
    if head in snake[1:]:
        return True
    return False

def check_collision_conway(grid, snake):
    for i in range(len(snake)):
        if grid[snake[i]] == 1:
            return snake[:i]
        return snake

def draw_snake(snake):
    pygame.draw.rect(screen, HEAD, (snake[0][0]*CELL_SIZE, snake[0][1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for (x, y) in snake[1:]:
        pygame.draw.rect(screen, BODY, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def generate_food(grid):
    col = random.randint(0, GRID_SIZE-1)
    row = random.randint(0, GRID_SIZE-1)
    while grid[row, col] != 0:
        pos = row*GRID_SIZE + col + 1
        row = pos // GRID_SIZE
        col = pos % GRID_SIZE
        if row >= GRID_SIZE:
            row = 0
    return tuple((col, row))

def generate_foods(grid, food_count):
    foods = []
    for _ in range(food_count):
        foods.append(generate_food(grid))
    return foods


def update_foods(grid, foods, food_count):
    count = 0
    new_foods = []
    for food in foods:
        if grid[food] != 0:
            count += 1
            new_food = generate_food(grid)
        else:
            new_food = food
        update_grid_food(grid, new_food)
        new_foods.append(new_food)

    while len(new_foods) < food_count:
        new_foods.append(generate_food(grid))
        update_grid_food(grid, foods[-1])

    return count, new_foods



def main():
    # Create the grid
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    running = True
    paused = False

    session_time = 10
    invincible_time = 3
    session_count = 1
    start_size = 9
    snake_dir = (-1, 0)
    queued_growth = 0
    score = 9

    snake = [(GRID_SIZE//2+i, GRID_SIZE//2) for i in range(start_size)]
    foods = generate_foods(grid, session_count)
    update_grid_snake(grid, snake)
    update_grid_food(grid, foods)

    st_time = time.time()
    time_count = 0

    screen.fill(BLACK)
    draw_cells(grid)
    draw_grid()
    while running:

        if not paused:
            time_count = time.time()-st_time
            if time_count >= session_time:  # session end, reborn
                session_count += 1
                new_grid = grid.copy()
                for segment in snake:
                    new_grid[segment] = 1

                snake = [(GRID_SIZE//2+i, GRID_SIZE//2) for i in range(start_size)]
                snake_dir = (-1, 0)

                st_time = time.time()
            else:  # normal game + invinc

                # get first event or null
                for event in pygame.event.get()[:1]:
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake_dir != (1, 0):
                            snake_dir = (-1, 0)
                        elif event.key == pygame.K_DOWN and snake_dir != (-1, 0):
                            snake_dir = (1, 0)
                        elif event.key == pygame.K_LEFT and snake_dir != (0, 1):
                            snake_dir = (0, -1)
                        elif event.key == pygame.K_RIGHT and snake_dir != (0, -1):
                            snake_dir = (0, 1)

                new_grid = update_grid_conway(grid)
                snake = move_snake(snake, snake_dir)

                # end game and print score if hit wall/self
                if check_collision(snake):
                    break

                # case: snake is invincible
                if time_count <= invincible_time:
                    global BODY
                    if session_count != 1:
                        if int((time_count*FPS) % 2) == 0:
                            BODY = (0, 255, 255)
                        else:
                            BODY = (255, 255, 0)
                else:
                    BODY = (0, 0, 255)
                    snake = check_collision_conway(new_grid, snake)
                    if len(snake) == 0:
                        break

                # cut tail if done growing
                if queued_growth == 0:
                    snake.pop()
                else:
                    queued_growth -= 1

                update_grid_snake(new_grid, snake)

                count, foods = update_foods(new_grid, foods, session_count)
                queued_growth += count

            grid = new_grid

        screen.fill(BLACK)
        draw_cells(grid)
        draw_grid()
        draw_time_label(screen, time_count)
        score = max(len(snake), score)
        draw_score_label(screen, score)
        pygame.display.flip()
        clock.tick(FPS)

    # pygame.quit()
    return score

if __name__ == '__main__':
    main()
