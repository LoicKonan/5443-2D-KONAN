import math

import pygame
from pygame import Vector2

from objects.GameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


class Explosion(GameObject):
    def __init__(self, pos):
        super().__init__(pos,None)

        self.animSheet = SpriteSheet(assetsManager.get("explo1"), 1, 10)
        self.animSheet.setPlay(0, 9, 0.07, False)
        self.img = self.animSheet.getCurrentFrame()


    def update(self):
        if self.animSheet.current >= 9:
            self.destroyFlag = True

        super().update()
        self.animSheet.play()
        self.img = self.animSheet.getCurrentFrame()

