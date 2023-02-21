import pygame
import random
import pygame.mixer
import words
import itertools

pygame.init()
pygame.mixer.init()

# screen setup Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

global KEY_WIDTH
global KEY_HEIGHT
global KEY_MARGIN

# screen setup size constants
WIDTH  = 600
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
letter_font = pygame.font.Font("assets/FreeSansBold.otf", 50)

# This is the KEY(CORRECT ANSWER).
# secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
secret_word = "ETHER"


# This is the game over.
game_over = False

# No letters has been entered yet.
letters = 0

# This is the turn active.
turn_active = True

# Define the dimensions of the keyboard
KEY_WIDTH = 40
KEY_HEIGHT = 40
KEY_MARGIN = 10


# set up the rotation angle and speed
angle = 0
rotate_speed = 5

# set up sound effects
win_sound  = pygame.mixer.Sound("assets/win.ogg")
lose_sound = pygame.mixer.Sound("assets/lost.mp3")


# This Function will draw the squares on the screen and determine the size and spaces.
def draw_board():
    global turn
    global board
    global piece_text
    for col, row in itertools.product(range(5), range(6)):
        pygame.draw.rect(screen, WHITE, [col * 80 + 100, row * 80 + 12, 65, 65], 2, 6)
        piece_text = huge_font.render(board[row][col], True, GRAY)
        screen.blit(piece_text, (col * 80 + 110, row * 80 + 12))

    # This indicate what turn you on (THE GREEN SQUARE).
    pygame.draw.rect(screen, GREEN, [82, turn * 80 + 5, WIDTH - 180, 77], 4, 10)

# This Function will check if the word is correct.
def check_words():
    global board
    global turn
    global secret_word
    
    # This will check if the word is correct.
    for col, row in itertools.product(range(5), range(6)):
        if secret_word[col] == board[row][col] and turn > row:
            pygame.draw.rect(screen, GREEN, [col * 80 + 100, row * 80 + 12, 65, 65], 0, 6)

        elif board[row][col] in secret_word and turn > row:
            pygame.draw.rect(screen, YELLOW, [col * 80 + 100, row * 80 + 12, 65, 65], 0, 6)

# game loop
running = True
while running:
    clock.tick(fps)
    screen.fill(BLACK)
    check_words()
    draw_board()

    for event in pygame.event.get():
        # This is the quit event.
        if event.type == pygame.QUIT:
            running = False

        # add player controls for letter entry, backspacing, checking guesses and restarting
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__('text')
            if entry != " ":
                entry = entry.upper()
                board[turn][letters] = entry
                letters += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = ' '
                letters -= 1
            if event.key == pygame.K_RETURN and not game_over:
                turn += 1
                letters = 0
            if event.key == pygame.K_RETURN and game_over:
                turn = 0
                letters = 0
                game_over = False
                secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]

        # control turn active based on letters
        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

        # check if guess is correct, add game over conditions
        for row in range(6):
            guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
            if guess == secret_word and row < 6: 
                game_over = True

        # This will print loser on the screen
        if turn == 6:
            game_over = True
            loser_text = letter_font.render('Loser!', True, WHITE)
            screen.blit(loser_text, (200, 490))
            # lose_sound.play()
            
            # Display the secret message below.
            secret_message = letter_font.render(secret_word, True, GREEN)
            screen.blit(secret_message, (200, 725))


        # This will print winner on the screen
        if game_over and turn < 6:
            winner_text = huge_font.render('Winner!', True, WHITE)
            screen.blit(winner_text, (200, 490))
            win_sound.play()

    pygame.display.flip()
pygame.quit()
