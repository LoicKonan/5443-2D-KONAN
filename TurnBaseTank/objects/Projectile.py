import math

import pygame
from pygame import Vector2

from objects.MiniProjectile import MiniProjectile
from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


class Projectile(GameObject):
    def __init__(self,pos,force,pType):
        self.animSheet = SpriteSheet(assetsManager.get("projectile"),1,7)
        self.animSheet.setPlay(0,6,0.01,True)
        super().__init__(pos,self.animSheet.getCurrentFrame(),pType)
        self.applyForce(force)
        print(force)
        self.angle = 0

        self.deathTime = 0

    def update(self):


        super().update()

        self.animSheet.play()
        self.rotate()

        self.deathTime += utils.deltaTime()
        if self.deathTime >= 100:
            self.destroy = True
        if self.pos.y >= 2000:
            self.destroy = True

    def getProjectiles(self):
        p1 = MiniProjectile(self.pos,self.type)
        p2 = MiniProjectile(self.pos, self.type)

        p1.vel = self.vel
        p2.vel = self.vel

        p1.applyForce(Vector2(-5,0))
        p2.applyForce(Vector2( 5, 0))

        return p1,p2


    def rotate(self):
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        a = angle
        angle -= 180
        self.angle = angle

    def draw(self):
        offset = Vector2(0, 0)
        rotated_image, rect = utils.rotate(self.animSheet.getCurrentFrame(), self.angle, [self.pos.x, self.pos.y], offset)
        self.img = rotated_image
        super().draw()