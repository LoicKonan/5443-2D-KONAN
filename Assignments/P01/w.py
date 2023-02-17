import itertools
import pygame

# Constants and variables with descriptive names
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50
FONT_PATH = "assets/FreeSansBold.otf"
ICON_PATH = "assets/Icon.png"
BOARD = [[" 4 ", " ", " ", " ", " "],
         [" ", " 5 ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " 8 ", " ", " 9 "],
         [" ", " ", " ", " ", " 1 "]]

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Wordle Game")
pygame.display.set_icon(pygame.image.load(ICON_PATH))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Functions to draw the board, handle events, and update the screen
def draw_board(turn):
    for col, row in itertools.product(range(5), range(6)):
        rect = pygame.draw.rect(screen, WHITE, [col * 80 + 100, row * 80 + 12, 65, 65], 2, 6)
        piece_text = font.render(BOARD[row][col], True, WHITE)
        screen.blit(piece_text, rect.topleft)
    pygame.draw.rect(screen, GREEN, [82, turn * 80 + 5, SCREEN_WIDTH - 180, 77], 4, 10)

def handle_events():
    return all(event.type != pygame.QUIT for event in pygame.event.get())

def update_screen():
    pygame.display.update()

# Game loop
def main():
    turn = 0
    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        draw_board(turn)
        running = handle_events()
        update_screen()

    pygame.quit()

if __name__ == "__main__":
    main()
