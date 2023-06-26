import math

from pygame import Vector2

from objects.Projectile.Projectile import Projectile
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


class PlayerProjectile(Projectile):
    def __init__(self,pos,vel,img):
        super().__init__(pos)
        self.img = img
        self.cDestroyTime = 0
        self.vel = vel
        self.damage = 1

    def update(self):
        self.cDestroyTime += utils.deltaTime()
        if self.cDestroyTime >= 2.0 :
            self.destroyFlag = True

        super().update()

    # def rotate(self):
    #     angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
    #     a = angle
    #     angle -= 0
    #     self.angle = angle
    #
    # def draw(self):
    #     rotated_image, rect = utils.rotate(self.img, self.angle, [self.pos.x, self.pos.y],Vector2(0, 0))
    #     self.img = rotated_image
    #     super().draw()


