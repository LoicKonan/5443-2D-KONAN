import pygame
import random

pygame.init()

# set up the display
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set up the font
font = pygame.font.SysFont('Arial', 36)

# set up the initial word and its position
word = ''
word_surface = font.render(word, True, (255, 255, 255))
word_rect = word_surface.get_rect(center=(WIDTH//2, HEIGHT//2))

# set up the rotation angle and speed
angle = 0
rotate_speed = 5

# set up the game clock
clock = pygame.time.Clock()

# set up the game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                word += event.unicode
                word_surface = font.render(word, True, (255, 255, 255))
                word_rect = word_surface.get_rect(center=(WIDTH//2, HEIGHT//2))

    # rotate the word surface
    angle += rotate_speed
    rotated_surface = pygame.transform.rotate(word_surface, angle)

    # draw the background and the rotated word
    screen.fill((0, 0, 0))
    screen.blit(rotated_surface, rotated_surface.get_rect(center=word_rect.center))

    # update the display
    pygame.display.flip()

    # tick the clock
    clock.tick(60)

pygame.quit()
