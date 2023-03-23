import pygame
from game import Game
from utils.util import utils

game = Game()

while True:
    utils.screen.fill((22, 122, 122), (0, 0, utils.width, utils.height))
    utils.initDeltaTime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            game.onKeyDown(event.key)
        if event.type == pygame.KEYUP:
            game.onKeyUp(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.onMouseDown(event)
        if event.type == pygame.MOUSEBUTTONUP:
            game.onMouseUp(event)

    game.update()
    game.draw()

    utils.showFps()

    pygame.display.flip()
