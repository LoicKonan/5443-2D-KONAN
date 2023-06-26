import pygame.rect
from pygame.math import Vector2

from objects.GameObject import GameObject
from utils.util import utils


class Wall(GameObject):

    def __init__(self, pos, img, visible = True):
        super().__init__(pos,img,visible)

    def wallCollide(self,player):
        if player.vel.y > 0:
            player.vel.y = 0
            player.jumping = False
            player.pos.y = player.prevPos.y
        elif player.vel.x != 0:
            player.vel.x = 0
            player.pos.x = player.prevPos.x

