import math
import pygame
from pygame import Vector2

from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils

class Explosion(GameObject):
    def __init__(self, pos):
        # Create a new SpriteSheet instance with the explosion animation image,
        # specifying the number of rows and columns in the image
        self.animSheet = SpriteSheet(assetsManager.get("explo1"), 1, 12)
        
        # specifying the start frame index, end frame index, frame duration, and whether the animation should loop
        self.animSheet.setPlay(0, 11, 0.1, False)
        
        # Call the __init__ method of the superclass (GameObject) with the initial position,
        # the current frame of the animation sheet, and the name of the object
        super().__init__(pos, self.animSheet.getCurrentFrame(), "explo")

    def update(self):
        # Call the update method of the superclass (GameObject) to update the position and velocity
        super().update()
        
        # Play the animation by calling the play method of the animation sheet
        self.animSheet.play()

    def draw(self):
        # Set the current frame of the animation sheet as the image to draw
        self.img = self.animSheet.getCurrentFrame()
        
        # Call the draw method of the superclass (GameObject) to draw the image at the current position
        super().draw()
