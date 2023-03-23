import pygame
import math
from pygame.locals import *

from pygame import Vector2

from utils.camera import Camera


class Utils():

    def __init__(self):
        pygame.init()

        self.height = 720
        self.width = 1280
        self.gameOver = False
        self.currentLevel = 0
        self.screen = pygame.display.set_mode((self.width, self.height),DOUBLEBUF,16)
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.fps = 0
        self.fpsCounter = 0
        self.fpsTimeCount = 0

        self.camera = Camera()

    def initDeltaTime(self):  # calculate deltaTime
        t = self.clock.tick(60)
        self.dt = t / 1000

    def deltaTime(self):
        return self.dt

    def showFps(self):
        self.fpsTimeCount += self.deltaTime()
        self.fpsCounter += 1
        if self.fpsTimeCount > 1:
            self.fpsTimeCount = 0
            self.fps = self.fpsCounter
            self.fpsCounter = 0

        if self.fps >= 50:
            self.drawText(Vector2(0,0),"fps: " + str(self.fps),(23,233,23),16)
        else:
            self.drawText(Vector2(0, 0), "fps: " + str(self.fps), (233, 23, 23), 16)

    def drawText(self, pos, text, color, size):  # draw text
        self.font = pygame.font.Font('assets/Merchant.ttf', size)
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

    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect


utils = Utils()  # util is global object
