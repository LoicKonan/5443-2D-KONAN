import pygame
from pygame import Vector2

from screens.Game import Game
from screens.MainGame import MainGame
from utils.Button import Button
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class MainMenu(Game):
    def __init__(self):
        self.buttons = []

        self.buttons.append(Button(0, Vector2(300, 200),"Start",Vector2(3,2)))
        self.buttons.append(Button(3, Vector2(300, 300), "Quit", Vector2(3, 2)))

        sounds.playMusic()

    def update(self):
        for button in self.buttons:
            if button.clicked:
                if button.id == 0:
                    utils.currentScreen = MainGame()
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


