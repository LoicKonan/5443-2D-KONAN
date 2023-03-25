import math

import pygame
from pygame import Vector2

from objects.MiniProjectile import MiniProjectile
from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


# A class for projectiles that extends GameObject
class Projectile(GameObject):
    def __init__(self,pos,force,pType):
        # Set up the sprite sheet animation
        self.animSheet = SpriteSheet(assetsManager.get("projectile"),1,7)
        self.animSheet.setPlay(0,6,0.01,True)
        
        # Call the super constructor to initialize the GameObject with the current frame and type
        super().__init__(pos,self.animSheet.getCurrentFrame(),pType)
        
        # Apply force to the projectile
        self.applyForce(force)
        print(force)
        
        # Initialize the angle and death time variables
        self.angle = 0
        self.deathTime = 0

    def update(self):
        # Call the update function of the super class
        super().update()
        # Play the animation
        self.animSheet.play()
        # Rotate the projectile
        self.rotate()

        # Increment the death time and destroy the projectile if it has lived too long or gone too far
        self.deathTime += utils.deltaTime()
        if self.deathTime >= 100:
            self.destroy = True
        if self.pos.y >= 2000:
            self.destroy = True

    # Create and return two mini projectiles with the missile's velocity and type.
    def getProjectiles(self):
        # Create two mini projectiles
        p1 = MiniProjectile(self.pos,self.type)
        p2 = MiniProjectile(self.pos, self.type)

        # Set the velocity of the mini projectiles to be the same as the velocity of the projectile
        p1.vel = self.vel
        p2.vel = self.vel

        # Apply a small force to the mini projectiles to give them a spread
        p1.applyForce(Vector2(-5,0))
        p2.applyForce(Vector2( 5, 0))

        return p1,p2

    # Rotate the projectile based on its velocity
    def rotate(self):
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        a = angle
        angle -= 180
        self.angle = angle

    # Draw the projectile to the screen
    def draw(self):
        # Set the offset to zero
        offset = Vector2(0, 0)
        # Rotate the image and get the new image and rectangle
        rotated_image, rect = utils.rotate(self.animSheet.getCurrentFrame(), self.angle, [self.pos.x, self.pos.y], offset)
        # Set the projectile's image to the rotated image
        self.img = rotated_image
        # Call the draw function of the super class
        super().draw()
