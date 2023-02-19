# Build a worlde game in pygame.
# This game should have flying in of letters when a word is entered
# display a keyboard on the screen
# display a loser to the screen if the player lose with a loser sound and ask him if he want to play again
# or if the player win it should display winner with a winner sound and if the player want to play again. 

import pygame
import random
import time
import sys
import os
import math
import string

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Title and Icon
pygame.display.set_caption("killer Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
    
# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_text = font.render("Score: " + str(score_value), 1, (255, 255, 255))

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_text = over_font.render("Game Over", 1, (255, 255, 255))

# Winner
winner_font = pygame.font.Font('freesansbold.ttf', 64)
winner_text = winner_font.render("Winner", 1, (255, 255, 255))

# Loser
loser_font = pygame.font.Font('freesansbold.ttf', 64)
loser_text = loser_font.render("Loser", 1, (255, 255, 255))

# Play Again
play_again_font = pygame.font.Font('freesansbold.ttf', 32)
play_again_text = play_again_font.render("Play Again", 1, (255, 255, 255))
