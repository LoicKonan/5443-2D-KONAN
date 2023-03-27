import pygame
import random
from game import Game
from utils.util import utils
pygame.font.init()

# Create a new Game instance
game = Game()

    
# Game loop
while True:
    # Set the background color of the screen to black    
    utils.screen.fill((0, 0, 0), (0, 0, utils.width, utils.height))

    # Initialize the delta time used for animation and movement updates
    utils.initDeltaTime()

    # Process all events in the Pygame event queue
    for event in pygame.event.get():
        # If the user closes the window, exit the program
        if event.type == pygame.QUIT:
            exit(0)
        # If a key is pressed, call the onKeyDown method in the Game instance with the key as an argument
        if event.type == pygame.KEYDOWN:
            game.onKeyDown(event.key)
        # If a key is released, call the onKeyUp method in the Game instance with the key as an argument
        if event.type == pygame.KEYUP:
            game.onKeyUp(event.key)
        # If the mouse button is pressed, call the onMouseDown method in the Game instance with the event as an argument
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.onMouseDown(event)
        # If the mouse button is released, call the onMouseUp method in the Game instance with the event as an argument
        if event.type == pygame.MOUSEBUTTONUP:
            game.onMouseUp(event)

    # Update the Game instance with the current delta time
    game.update()

    # Draw the current frame using the Game instance
    game.draw()

    # # Display the current frame rate on the screen
    # utils.showFps()

    # Update the screen with the new frame
    pygame.display.flip()
