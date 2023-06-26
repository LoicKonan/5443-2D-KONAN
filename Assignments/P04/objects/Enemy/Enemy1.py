import pygame
from pygame.math import Vector2

from objects.Enemy.Enemy import Enemy
from objects.HealthBar import HealthBar
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


class Enemy1(Enemy):
    def __init__(self,pos,dest):
        super().__init__(pos)
        self.walkSheet = SpriteSheet(assetsManager.get("enemy1"),2,7)
        self.walkSheet.setPlay(0,6,0.07,True)
        self.currentSheet = self.walkSheet
        self.speed = 2
        self.cFlipDirTime = 0
        self.damage = 1
        self.health = 20
        self.img = self.currentSheet.getCurrentFrame()
        self.healthBar = HealthBar(self.health, (233, 23, 23), self.getRect().w + 4)

        self.start = Vector2(pos.x, pos.y)
        self.dest = dest


    def update(self):
        self.currentSheet.play()
        self.img = self.currentSheet.getCurrentFrame()
        self.pos.x += self.speed

        if utils.distance(self.pos.x, self.pos.y, self.dest.x, self.dest.y) <= 10:
            tmp = Vector2(self.start.x, self.start.y)
            self.start = Vector2(self.dest.x, self.dest.y)
            self.dest = tmp
            self.speed *= -1

        if self.speed > 0:
            self.flipX = True
        else:
            self.flipX = False

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x + 20, self.pos.y + 20, self.img.get_width() - 40, self.img.get_height()-40)
        return rect

    def draw(self):
        super().draw()
        self.healthBar.draw(self.health, Vector2(self.getRect().x, self.getRect().y - 12))
