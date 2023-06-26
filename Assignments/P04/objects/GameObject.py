import pygame.rect
from pygame.math import Vector2
from utils.util import utils

from enum import Enum


class GameObject:

    def __init__(self, pos, img, visible=True):
        self.pos = pos
        self.img = img
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.destroyFlag = False
        self.visible = visible
        self.flipX = False
        self.health = -1
        self.damage = -1
        self.healthBar = None

    def update(self):
        self.vel = Vector2(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        self.pos = Vector2(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        self.acc = Vector2(0, 0)

    def applyForce(self, f):
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def hit(self,obj):
        self.health -= obj.damage
        if self.health <= 0 :
            self.destroyFlag = True

    def draw(self):
        if not self.visible:
            return

        if self.flipX:
            self.img = pygame.transform.flip(self.img, True, False)

        utils.screen.blit(self.img, (self.pos.x - utils.camera.x, self.pos.y - utils.camera.y))

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        return rect

    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def getCenter(self):
        return Vector2(self.pos.x + self.getRect().w / 2, self.pos.y + self.getRect().h / 2)
