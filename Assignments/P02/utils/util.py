import pygame
import math
from pygame.locals import *
from pygame import Vector2
from utils.camera import Camera
pygame.font.init()


class Utils():
    
    # Initialize the Utils class and set some default values
    def __init__(self):
        pygame.init()
        
        # set the game window size and initialize game variables
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
        
        # create a camera object
        self.camera = Camera()

    # Method to calculate deltaTime
    def initDeltaTime(self):  
        t = self.clock.tick(60)
        self.dt = t / 1000

    # Method to return deltaTime
    def deltaTime(self):
        return self.dt

    # Method to show frames per second (fps) on the screen
    def showFps(self):
        # calculate fps
        self.fpsTimeCount += self.deltaTime()
        self.fpsCounter += 1
        if self.fpsTimeCount > 1:
            self.fpsTimeCount = 0
            self.fps = self.fpsCounter
            self.fpsCounter = 0

        # draw fps on screen
        if self.fps >= 50:
            self.drawText(Vector2(0,0),"fps: " + str(self.fps),(23,233,23),16)
        else:
            self.drawText(Vector2(0, 0), "fps: " + str(self.fps), (233, 23, 23), 16)

    # Method to draw text on the screen
    def drawText(self, pos, text, color, size):  
        self.font = pygame.font.Font('assets/FreeSansBold.otf', size)
        text = self.font.render(text, True, color)
        self.screen.blit(text, (pos.x, pos.y))
   
        
        


    # Method to calculate distance between two points
    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0);

    # Method to check for  collision between two boxes
    def collide(self, a, b):  
        rect = a.getRect()
        r = b.getRect()
        return (
            r.x < rect.x + rect.w
            and r.x + r.w > rect.x
            and r.y < rect.y + rect.h
            and r.h + r.y > rect.y
        )


    # Method to rotate a surface around a pivot point
    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect

# Global Utils object
utils = Utils() 
