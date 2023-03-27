import math
import pygame
from pygame import Vector2

from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils

class MiniProjectile(GameObject):
    def __init__(self,pos,pType):
        # initialize the projectile with an animation sheet and type
        self.animSheet = SpriteSheet(assetsManager.get("projectile"), 1, 7)
        self.animSheet.setPlay(0, 6, 0.01, True)
        super().__init__(pos,self.animSheet.getCurrentFrame(),pType)
        self.angle = 0

        # set a death time and initialize it to zero
        self.deathTime = 0

    def update(self):
        super().update()
        # play the animation sheet
        self.animSheet.play()
        # rotate the projectile
        self.rotate()

        # increase the death time by the time elapsed since last frame
        self.deathTime += utils.deltaTime()
        # destroy the projectile if the death time has exceeded a certain value
        if self.deathTime >= 3:
            self.destroy = True
        # destroy the projectile if it has gone off the screen
        if self.pos.y >= 721:
            self.destroy = True

    def rotate(self):
        # calculate the angle of the projectile based on its velocity
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        a = angle
        # flip the angle by 180 degrees to orient it correctly
        angle -= 180
        self.angle = angle

    def draw(self):
        # rotate the image of the projectile based on the angle calculated in rotate()
        offset = Vector2(0, 0)
        rotated_image, rect = utils.rotate(self.animSheet.getCurrentFrame(), self.angle, [self.pos.x, self.pos.y], offset)
        # scale the rotated image
        rotated_image = pygame.transform.scale(rotated_image,(20,20))
        self.img = rotated_image
        # draw the projectile on the screen
        super().draw()
