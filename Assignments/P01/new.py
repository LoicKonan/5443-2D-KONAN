import pygame
import sys
import random
import pygame.mixer
from lists import *
import itertools
import pygame


pygame.init()
pygame.mixer.init()


# screen setup Colors
white  = (255, 255, 255)
black  = (0, 0, 0)
green  = (0, 255, 0)
yellow = (255, 255, 0)
gray   = (128, 128, 128)

# screen setup size constants
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# screen Title and Icon Image.
pygame.display.set_caption("Wordle Game")
ICON = pygame.image.load("assets/Icon.png")
pygame.display.set_icon(ICON)

# screen square 6 x 5 matrix
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

# This is the turn.
turn = 0

# This is the frame rate.
fps = 60

# This is the clock.
clock = pygame.time.Clock()

# This is the font.
huge_font = pygame.font.Font("assets/FreeSansBold.otf", 56)

# This is the secret word.
secret_word = "ETHER"

# This is the game over.
game_over = False

# No letters has been entered yet.
letters = 0

# This is the turn active.
turn_active = True

# This Function will draw the squares on the screen and determine the size and spaces.
def draw_board():
    global turn
    global board
    for col, row in itertools.product(range(5), range(6)):
        pygame.draw.rect(screen, white, [col * 80 + 100, row * 80 + 12, 65, 65], 2, 6)
        piece_text = huge_font.render(board[row][col], True, gray)
        screen.blit(piece_text, (col * 80 + 110, row * 80 + 12))

    # This indicate what turn you on.
    pygame.draw.rect(screen, green, [82, turn * 80 + 5, WIDTH - 180, 77], 4, 10)


def check_words():
    global board
    global turn
    global secret_word

    # This will check if the word is correct.
    for col, row in itertools.product(range(5), range(6)):
        if secret_word[col] == board[row][col] and turn > row:
            pygame.draw.rect(screen, green, [col * 80 + 100, row * 80 + 12, 65, 65], 0, 6)

        elif board[row][col] in secret_word and turn > row:
            pygame.draw.rect(screen, yellow, [col * 80 + 100, row * 80 + 12, 65, 65], 0, 6)
            



# game loop
running = True

while running:
    clock.tick(fps)
    screen.fill(black)
    check_words()
    draw_board()

    for event in pygame.event.get():

        # This is the quit event.
        if event.type == pygame.QUIT:
            running = False

        # 
        if event.type == pygame.KEYDOWN:
            
            # This is the backspace event.
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = " "
                letters -= 1
               
            # This is will check if space button or the enter key is pressed 
            # and that the game is not over then move to the next turn.
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN and not game_over:
                turn += 1
                letters = 0
                turn_active = True

        # 
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__('text')
            print(event)
            board[turn][letters] = entry
            letters += 1


        # This is the turn change.
        if letters == 5:
            turn_active = False

        if letters < 5:
            turn_active = True
       

    # This is the update event.
    pygame.display.update()

# This is the quit event.
pygame.quit()
