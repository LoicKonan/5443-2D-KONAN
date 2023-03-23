import pygame.rect
from pygame.math import Vector2
from utils.util import utils


class GameObject:

    def __init__(self, pos, img, type=""):
        self.pos = pos
        self.img = img
        self.type = type

        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.destroy = False

    def update(self):
        self.vel = Vector2(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        self.pos = Vector2(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        self.acc = Vector2(0, 0)

    def applyForce(self, f):
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def draw(self):
        utils.screen.blit(self.img, (self.pos.x - utils.camera.pos.x, self.pos.y - utils.camera.pos.y))

    def getRect(self):  # get the rectangle box of object
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        return rect

    def setPos(self, pos):
        self.pos = pos

    def onWallCollide(self, player):
        wallRect = self.getRect()
        wallRect.w += 4
        wallRect.h += 4
        playerRect = player.getRect()
        # if self.timeToflip != 0:
        #     player.pos = Vector2((player.pos.x + self.vel.x), player.pos.y)
        # wall collide with player , top ,left,right, bottom
        # top
        if playerRect.y + playerRect.height > wallRect.y > playerRect.y:
            diff = playerRect.y + playerRect.height - wallRect.y
            player.vel = Vector2(player.vel.x, 0)
            player.setOnGround(True)
            player.setPos(Vector2(player.pos.x, playerRect.y - diff ))
        # left
        elif playerRect.y + playerRect.height < wallRect.y + wallRect.height and playerRect.x + playerRect.width > wallRect.x > playerRect.x:
            diff = playerRect.x + playerRect.width - wallRect.x
            player.setPos(Vector2(playerRect.x - diff, playerRect.y))
            player.vel = Vector2(0, player.vel.y)
        # right
        elif playerRect.y + playerRect.height < wallRect.y + wallRect.height and playerRect.x < wallRect.x + wallRect.width and playerRect.x + playerRect.width > wallRect.x:
            diff = wallRect.x + wallRect.width - playerRect.x
            player.setPos(Vector2(playerRect.x + diff, playerRect.y))
            player.vel = Vector2(0, player.vel.y)
        # bottom
        elif wallRect.y + wallRect.height > playerRect.y > wallRect.y:
            diff = wallRect.y + wallRect.height - playerRect.y
            player.vel = Vector2(player.vel.x, 0)
            player.setPos(Vector2(player.pos.x, playerRect.y + diff + 2))
