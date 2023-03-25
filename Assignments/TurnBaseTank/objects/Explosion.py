import math

import pygame
from pygame import Vector2

from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


##############################################################################################
# class Explosion(GameObject):
#
#   - This program defines a class Explosion that extends from GameObject. 
#   - The  __init__ method that initializes an animation sprite sheet from an image file, 
#   - sets the play range and animation speed, and then calls the superclass constructor 
#   - with the initial position, the current animation frame, and a name.
#   - The update and draw methods that respectively update the animation state 
#   - and render the current frame. The update method calls the superclass update method 
#   - and then updates the animation state with the play method.

##############################################################################################

class Explosion(GameObject):
    def __init__(self, pos):
        self.animSheet = SpriteSheet(assetsManager.get("explo1"), 1, 12)
        self.animSheet.setPlay(0, 11, 0.1, False)
        super().__init__(pos, self.animSheet.getCurrentFrame(), "explo")

    def update(self):
        super().update()
        self.animSheet.play()

    def draw(self):
        self.img = self.animSheet.getCurrentFrame()
        super().draw()
