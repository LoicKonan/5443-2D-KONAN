import pygame.rect
from pygame.math import Vector2
from utils.util import utils


class GameObject:

    def __init__(self, pos, img, type=""):
        # Initialize position, image, and type attributes
        self.pos  = pos
        self.img  = img
        self.type = type

        # Initialize velocity, acceleration, and destroy attributes
        self.vel  = Vector2(0, 0)
        self.acc  = Vector2(0, 0)
        self.destroy = False

    def update(self):
        # Update velocity and position based on acceleration
        self.vel = Vector2(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        self.pos = Vector2(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        # Reset acceleration to zero
        self.acc = Vector2(0, 0)

    def applyForce(self, f):
        # Add force to acceleration
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def draw(self):
        # Draw image at position adjusted by camera position
        utils.screen.blit(self.img, (self.pos.x - utils.camera.pos.x, self.pos.y - utils.camera.pos.y))

    def getRect(self):  
        # get the rectangle box of object
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        return rect

    def setPos(self, pos):
        # Set position attribute
        self.pos = pos

    def onWallCollide(self, player):
        # Create enlarged rectangles for wall and player collisions
        wallRect = self.getRect()
        wallRect.w += 4
        wallRect.h += 4
        playerRect = player.getRect()
       
        
        # top
        if playerRect.y + playerRect.height > wallRect.y > playerRect.y:
            # Calculate difference in y position between player and wall
            diff = playerRect.y + playerRect.height - wallRect.y
            # Stop player's y velocity and set onGround attribute to True
            player.vel = Vector2(player.vel.x, 0)
            player.setOnGround(True)
            # Set player's position just above the wall
            player.setPos(Vector2(player.pos.x, playerRect.y - diff ))
            
        # left
        elif playerRect.y + playerRect.height < wallRect.y + wallRect.height and playerRect.x + playerRect.width > wallRect.x > playerRect.x:
            # Calculate difference in x position between player and wall
            diff = playerRect.x + playerRect.width - wallRect.x
            # Set player's position just to the left of the wall
            player.setPos(Vector2(playerRect.x - diff, playerRect.y))
            # Stop player's x velocity
            player.vel = Vector2(0, player.vel.y)
            
        # right
        elif playerRect.y + playerRect.height < wallRect.y + wallRect.height and playerRect.x < wallRect.x + wallRect.width and playerRect.x + playerRect.width > wallRect.x:
            # Calculate difference in x position between player and wall
            diff = wallRect.x + wallRect.width - playerRect.x
            # Set player's position just to the right of the wall
            player.setPos(Vector2(playerRect.x + diff, playerRect.y))
            # Stop player's x velocity
            player.vel = Vector2(0, player.vel.y)
            
        # bottom
        elif wallRect.y + wallRect.height > playerRect.y > wallRect.y:
            # Calculate difference in y position between player and wall
            diff = wallRect.y + wallRect.height - playerRect.y
            # Stop player's y velocity
            player.vel = Vector2(player.vel.x, 0)
            # Set player's position just below the wall
            player.setPos(Vector2(player.pos.x, playerRect.y + diff + 2))
