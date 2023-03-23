import math
import random

import pygame
from pygame import Vector2

from objects.MiniProjectile import MiniProjectile
from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class Missile(GameObject):
    def __init__(self, pos, force, pType):
        self.animSheet = SpriteSheet(assetsManager.get("missile"), 8, 8)
        self.animSheet.setPlay(0, 60, 0.001, True)
        super().__init__(pos, self.animSheet.getCurrentFrame(), pType)
        self.applyForce(force)
        print(force)
        self.angle = 0

        self.deathTime = 0

        self.cc = 0
        self.target = None
        self.currentTarget = None
        self.randomTargets = []

        self.follow = False


    def applyForce(self, f):
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def update(self):

        if self.target.pos.x > 700:
            if utils.distance(self.pos.x, self.pos.y, self.target.pos.x + 500, self.target.pos.y + 32) < 1000:
                self.follow = True
        else:
            if utils.distance(self.pos.x, self.pos.y, self.target.pos.x - 500, self.target.pos.y + 32) < 1000:
                self.follow = True

        if self.follow:
            sounds.play("missile")
            self.moveTo(self.randomTargets[self.currentTarget])
            if self.currentTarget < 2 and \
                    utils.distance(self.pos.x, self.pos.y, self.randomTargets[self.currentTarget].x, self.randomTargets[self.currentTarget].y ) < 100:
                self.currentTarget += 1

        super().update()
        self.animSheet.play()
        self.rotate()

        self.deathTime += utils.deltaTime()
        if self.deathTime >= 100:
            self.destroy = True
        if self.pos.y >= 2000:
            self.destroy = True

    def moveTo(self,target):
        maxVel = 1000000
        maxForce = 1.5
        maxSpeed = 15

        nor = Vector2(target.x - self.pos.x, target.y - self.pos.y).normalize()
        desired_velocity = Vector2(nor.x * maxVel, nor.y * maxVel)
        steering = Vector2(desired_velocity.x - self.vel.x, desired_velocity.y - self.vel.y)
        steering.scale_to_length(maxForce)
        self.vel = Vector2(self.vel.x + steering.x, self.vel.y + steering.y)
        self.vel.scale_to_length(maxSpeed)
        self.pos.x = self.pos.x + self.vel.x
        self.pos.y = self.pos.y + self.vel.y

    def getProjectiles(self):
        p1 = MiniProjectile(self.pos, self.type)
        p2 = MiniProjectile(self.pos, self.type)

        p1.vel = self.vel
        p2.vel = self.vel

        p1.applyForce(Vector2(-5, 0))
        p2.applyForce(Vector2(5, 0))

        return p1, p2

    def rotate(self):
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        a = angle
        angle += 0
        self.angle = angle

    def draw(self):
        offset = Vector2(0, 0)
        rotated_image, rect = utils.rotate(self.animSheet.getCurrentFrame(), self.angle, [self.pos.x, self.pos.y],
                                           offset)
        self.img = rotated_image
        super().draw()

    def setTarget(self,target):
        self.target = target
        self.randomTargets.append(Vector2(target.pos.x + random.randrange(-200,300),target.pos.y - 700))
        self.randomTargets.append(Vector2(target.pos.x + random.randrange(-200,300),target.pos.y - 900))
        self.randomTargets.append(Vector2(self.target.pos.x + 32, self.target.pos.y + 32))
        self.currentTarget = 0