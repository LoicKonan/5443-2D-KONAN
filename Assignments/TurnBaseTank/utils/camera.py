import pygame
from pygame import Vector2


class Camera:
    def __init__(self):
        self.pos = Vector2(150, 0)
        self.target = None

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x - 1280 / 2, self.pos.y - 720 / 2, 1280, 720)
        return rect

    def update(self):
        if self.target is not None:
            self.pos.x = self.target.pos.x - 1280/2
            self.pos.y = self.target.pos.y - 720/2 + 200
        else:
            self.pos = Vector2(150, 0)

    def follow(self, target):
        self.target = target
