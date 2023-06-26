import pygame.rect
from pygame.math import Vector2

from objects.GameObject import GameObject
from objects.Wall.Wall import Wall
from utils.assets_manager import assetsManager
from utils.util import utils


class MovingWall(Wall):

    def __init__(self, pos,dest):
        super().__init__(pos,assetsManager.get("movingWall"),True)
        self.speed = -2
        self.start = Vector2(pos.x,pos.y)
        self.dest = dest

    def update(self):
        self.pos.x += self.speed
        if utils.distance(self.pos.x,self.pos.y,self.dest.x,self.dest.y) <= 10:
            tmp = Vector2(self.start.x,self.start.y)
            self.start = Vector2(self.dest.x,self.dest.y)
            self.dest = tmp
            self.speed *= -1

    def wallCollide(self,player):
        super().wallCollide(player)
        player.pos.x += self.speed

