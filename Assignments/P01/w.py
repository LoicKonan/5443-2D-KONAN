# Building Wordle Game!!!
import pygame
import sys
import random
import pygame.mixer
from lists import *
import itertools
import pygame

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WIDTH = 600
HEIGHT = 800
FPS = 60
BOARD_SIZE = 5
SQUARE_SIZE = 65
LINE_THICKNESS = 2
LINE_RADIUS = 6
FONT_SIZE = 50

# screen square 6 x 5 matrix
board = [["4", " ", " ", " ", " "],
         [" ", "5", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", "8", " ", "9"],
         [" ", " ", " ", " ", "1"]]


turn = 0

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Game")
ICON = pygame.image.load("assets/Icon.png") 
pygame.display.set_icon(ICON)

# Load font
with open("assets/FreeSansBold.otf", "rb") as f:
    huge_font = pygame.font.Font(f, FONT_SIZE)

# # Functions
# def draw_board() -> None:
#     for col, row in itertools.product(range(BOARD_SIZE), range(6)):
#         x = col * SQUARE_SIZE + 100
#         y = row * SQUARE_SIZE + 12
#         pygame.draw.rect(screen, WHITE, [x, y, SQUARE_SIZE, SQUARE_SIZE], LINE_THICKNESS, LINE_RADIUS)
#         text = huge_font.render(board[row][col], True, WHITE)
#         screen.blit(text, (x, y))

#     pygame.draw.rect(screen, GREEN, [82, turn * SQUARE_SIZE + 5, WIDTH - 180, 77], LINE_THICKNESS, LINE_RADIUS)
# This Function will draw the squares on the screen and determine the size and spaces.
def draw_board():
    global turn
    global board
    for col, row in itertools.product(range(5), range(6)):
        pygame.draw.rect(screen, WHITE, [col * 80 + 100, row * 80 + 12, 65, 65], 2, 6)
        piece_text = huge_font.render(board[row][col], True, WHITE)
        screen.blit(piece_text, (col * 80 + 100, row * 80 + 12))
        
    # This indicate what turn you on.
    pygame.draw.rect(screen, GREEN, [82, turn * 80 + 5, WIDTH - 180, 77], 4, 10)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
