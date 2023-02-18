# CODE YOUR OWN WORDLE IN 60 SECONDS
# import your modules
import random
import pygame
import words
pygame.init()

# create screen, fonts, colors, game variables
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Wordle Knockoff')
turn = 0
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('freesansbold.ttf', 56)
secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
game_over = False
letters = 0
turn_active = True

# create routine for drawing the board

def draw_board():
    global turn
    global board
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
            piece_text = huge_font.render(board[row][col], True, gray)
            screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
    pygame.draw.rect(screen, green, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 5)

# create routine for checking letters

def check_words():
    global turn
    global board
    global secret_word
    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)


# set up your main game loop

running = True
while running:
    timer.tick(fps)
    screen.fill(black)
    check_words()
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# add player controls for letter entry, backspacing, checking guesses and restarting

        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
                entry = event.__getattribute__('text')
                if entry != " ":
                    entry = entry.lower()
                    board[turn][letters] = entry
                    letters += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = ' '
                letters -= 1
            if event.key == pygame.K_SPACE and not game_over:
                turn += 1
                letters = 0
            if event.key == pygame.K_SPACE and game_over:
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

        for row in range(0, 6):
            guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
            if guess == secret_word and row < turn:
                game_over = True

        if turn == 6:
            game_over = True
            loser_text = huge_font.render('Loser!', True, white)
            screen.blit(loser_text, (40, 610))

        if game_over and turn < 6:
            winner_text = huge_font.render('Winner!', True, white)
            screen.blit(winner_text, (40, 610))


    pygame.display.flip()
pygame.quit()