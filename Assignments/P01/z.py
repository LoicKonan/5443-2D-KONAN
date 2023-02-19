import pygame
import sys
import random
import pygame.mixer
import words
import itertools

# Initialize Pygame and Pygame Mixer
pygame.init()
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Define screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set window title and icon
pygame.display.set_caption("Wordle Game")
ICON = pygame.image.load("assets/Icon.png")
pygame.display.set_icon(ICON)

# Set up game board
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

# Initialize game variables
current_turn = 0
fps = 60
clock = pygame.time.Clock()
huge_font = pygame.font.Font("assets/FreeSansBold.otf", 56)
letter_font = pygame.font.Font("assets/FreeSansBold.otf", 50)
secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
game_over = False
letters_entered = 0
turn_active = True

# set up sound effects
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")


# Define the dimensions of the keyboard
KEY_WIDTH = 40
KEY_HEIGHT = 40
KEY_MARGIN = 10

# Define the alphabet
ALPHABET = [" QWERTYUIOP ", " ASDFGHJKL  ", "  ZXCVBNM   "]

def draw_board():
    # Draw the squares on the screen and determine the size and spaces.
    global current_turn
    global board
    for col, row in itertools.product(range(5), range(6)):
        square = pygame.Rect(col * 80 + 100, row * 80 + 12, 65, 65)
        pygame.draw.rect(screen, WHITE, square, 2, 6)
        square_text = huge_font.render(board[row][col], True, GRAY)
        screen.blit(square_text, (col * 80 + 110, row * 80 + 12))

    # Indicate which turn you're on with a green square
    turn_square = pygame.Rect(82, current_turn * 80 + 5, SCREEN_WIDTH - 180, 77)
    pygame.draw.rect(screen, GREEN, turn_square, 4, 10)

def draw_keyboard(screen):
    # Set the font and font size
    font = pygame.font.Font("assets/FreeSansBold.otf", 36)

    # Draw the keys for each row of the keyboard
    y = 580
    for row in ALPHABET:
        x = 5

        for char in row:
            # Create a rectangular button for each key
            key = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)

            # Draw the key and outline
            pygame.draw.rect(screen, WHITE, key)
            pygame.draw.rect(screen, GRAY, key, 1)

            # Draw the character on the key
            text = font.render(char, True, BLACK)
            text_rect = text.get_rect(center=key.center)
            screen.blit(text, text_rect)

            x += KEY
