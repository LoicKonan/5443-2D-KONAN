import pygame
import math
from pygame.locals import *

from pygame import Vector2


class MUtils():

    def __init__(self):
        pygame.init()

        self.height = 600
        self.width = 800
        self.gameOver = False
        self.currentLevel = 0
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF, 16)
        self.dt = 0
        self.clock = pygame.time.Clock()

    def initDeltaTime(self):  # calculate deltaTime
        t = self.clock.tick(60)
        self.dt = t / 1000

    def deltaTime(self):
        return self.dt

    def drawText(self, pos, text, color, size):  # draw text
        self.font = pygame.font.Font('../assets/Unicorn.ttf', size)
        text = self.font.render(text, True, color)
        self.screen.blit(text, (pos.x, pos.y))

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0);

    def collide(self, a, b):  # aabb 2 box collide check
        rect = a.getRect()
        r = b.getRect()
        if r.x < rect.x + rect.w and r.x + r.w > rect.x and r.y < rect.y + rect.h and r.h + r.y > rect.y:
            return True
        return False


mUtils = MUtils()
