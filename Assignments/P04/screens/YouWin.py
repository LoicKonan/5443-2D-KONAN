import pygame
from pygame import Vector2

from screens.Game import Game
from utils.Button import Button
from utils.assets_manager import assetsManager
from utils.util import utils


class YouWin(Game):
    def __init__(self):
        self.buttons = []

        self.buttons.append(Button(0, Vector2(300, 200),"You Win!",Vector2(3,2)))
        self.buttons.append(Button(3, Vector2(300, 500), "Quit", Vector2(3, 2)))

    def update(self):
        for button in self.buttons:
            if button.clicked:
                if button.id == 0:
                    break
                if button.id == 3:
                    exit(1)

    def draw(self):

        for button in self.buttons:
            button.draw()

    def onKeyDown(self, key):
        pass

    def onKeyUp(self, key):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseUp(self, event):
        pass


