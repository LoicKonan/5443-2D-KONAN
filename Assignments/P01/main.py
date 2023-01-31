import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define block size
block_size = 30

# Define game window size
width = 10 * block_size
height = 20 * block_size

# Initialize pygame
pygame.init()

# Set game window size
screen = pygame.display.set_mode((width, height))

# Set game window title
pygame.display.set_caption("Tetris")

# Set game clock
clock = pygame.time.Clock()

# Define tetrominoes
tetrominoes = [[0, 1, 0],[1, 1, 1]], 
[[2, 2],[2, 2]], [[0, 3, 0],[0, 3, 0],[3, 3, 0]], 
[[0, 4, 0],[0, 4, 0],[0, 4, 4]], [[0, 5, 0],[0, 5, 0],[5, 5, 5]], 
[[6, 6, 0],[0, 6, 6],[0, 0, 0]]

# Define tetromino colors
colors = [RED, GREEN, WHITE, RED, GREEN, WHITE, RED]

# Function to create a new tetromino
def new_tetromino():
    tetromino = random.choice(tetrominoes)
    return tetromino

# Function to check if a tetromino can be placed in a given position
def valid_space(grid, tetromino, x, y):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell == 0:
                continue
            if y + i >= 20 or x + j < 0 or x + j >= 10:
                return False
            if grid[y + i][x + j] != 0:
                return False
    return True

# Function to merge tetromino into the grid
def merge_tetromino(grid, tetromino, x, y):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell == 0:
                continue
            grid[y + i][x + j] = cell

# Function to remove completed rows and update the score
def remove_complete_rows(grid, score):
    num_of_rows = 0
    for i, row in enumerate(grid[::-1]):
        if 0 not in row:
            num_of_rows += 1
            grid.pop(len(grid) - i - 1)
            grid = [[0 for j in range(10)]] + grid
    score += num_of_rows ** 2
    return score


# Initialize grid, tetromino, position and score
grid = [[0 for j in range(10)] for i in range(20)]
tetromino = new_tetromino()
x = 4
y = 0
score = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move tetromino down one block if possible, otherwise merge into the grid and choose a new tetromino
    if valid_space(grid, tetromino, x, y + 1):
        y += 1
    else:
        merge_tetromino(grid, tetromino, x, y)
        score = remove_complete_rows(grid, score)
        tetromino = new_tetromino()
        x = 4
        y = 0

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move tetromino left or right if possible
    if keys[pygame.K_LEFT] and valid_space(grid, tetromino, x - 1, y):
        x -= 1
    if keys[pygame.K_RIGHT] and valid_space(grid, tetromino, x + 1, y):
        x += 1

    # Rotate tetromino if possible
    if keys[pygame.K_UP]:
        tetromino_rotation = [list(reversed(row)) for row in zip(*tetromino)]
        if valid_space(grid, tetromino_rotation, x, y):
            tetromino = tetromino_rotation

    # Drop tetromino if possible
    if keys[pygame.K_DOWN]:
        while valid_space(grid, tetromino, x, y + 1):
            y += 1

    # Clear screen and draw grid, tetromino and score
    screen.fill(BLACK)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 0:
                continue
            color = colors[cell - 1]
            pygame.draw.rect(screen, color, (j * block_size,
                             i * block_size, block_size, block_size), 0)
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell == 0:
                continue
            color = colors[cell - 1]
            pygame.draw.rect(screen, color, ((x + j) * block_size,(y + i) * block_size, block_size, block_size), 0)
    label = pygame.font.SysFont("Comic Sans MS", 30).render("Score: " + str(score), 1, WHITE)
    screen.blit(label, (width - 150, height - 40))
    pygame.display.update()
    clock.tick(30)

# Quit game
pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
