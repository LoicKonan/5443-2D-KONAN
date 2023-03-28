import pygame
from pygame import Vector2


class Camera:
    def __init__(self):
        # Set the initial position of the camera    
        self.pos = Vector2(150, 0)
        # Set the initial target to None
        self.target = None

    def getRect(self):
        # Create a rectangle that represents the camera's view
        rect = pygame.rect.Rect(self.pos.x - 1180 / 2, self.pos.y - 620 / 2, 1180, 620)
        return rect

    def update(self):
        # If the camera has a target, set the camera's position to the target's 
        # position minus half of the screen width and height
        # plus 200 pixels to account for the player's height
        if self.target is not None:
            self.pos.x = self.target.pos.x - 1180/2
            self.pos.y = self.target.pos.y - 620/2 + 200
            
        # If the camera does not have a target, set its position to the initial position (150, 0)
        else:
            self.pos = Vector2(150, 0)

    def follow(self, target):
        # Set the target for the camera to follow
        self.target = target
