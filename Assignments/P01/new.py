# Building Wordle Game!!!
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
green = (0, 255, 0)

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

turn = 0
fps = 60
clock = pygame.time.Clock()
huge_font = pygame.font.Font("assets/FreeSansBold.otf", 50)
secret_word = "ETHER"

# This Function will draw the squares on the screen and determine the size and spaces.
def draw_board():
    global turn
    global board
    for col, row in itertools.product(range(5), range(6)):
        pygame.draw.rect(screen, white, [col * 80 + 100, row * 80 + 12, 65, 65], 2, 6)
        piece_text = huge_font.render(board[row][col], True, white)
        screen.blit(piece_text, (col * 80 + 100, row * 80 + 12))
        
    # This indicate what turn you on.
    pygame.draw.rect(screen, green, [82, turn * 80 + 5, WIDTH - 180, 77], 4, 10)
                
                
                
# game loop
running = True
while running:
    clock.tick(fps)
    screen.fill(black)
    draw_board()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    
pygame.quit()
