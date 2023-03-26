import math
import random

import pygame
from pygame import Vector2

from objects.MiniProjectile import MiniProjectile
from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class Missile(GameObject):
    def __init__(self, pos, force, pType):
       
        # Initialize the missile's sprite sheet animation, position, and type.
        self.animSheet = SpriteSheet(assetsManager.get("missile"), 8, 8)
        self.animSheet.setPlay(0, 60, 0.001, True)
        super().__init__(pos, self.animSheet.getCurrentFrame(), pType)
        
        # Apply the initial force to the missile.
        self.applyForce(force)
        print(force)
        
        # Set the missile's initial angle, death time, and tracking information.
        self.angle = 0
        self.deathTime = 0
        self.cc = 0
        self.target = None
        self.currentTarget = None
        self.randomTargets = []
        self.follow = False


    def applyForce(self, f):
        # Add a force vector to the missile's acceleration.
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    def update(self):
        # Check if the target is on the right side of the screen
        if self.target.pos.x > 700:
            # if so, check if the missile is within 1000 pixels of the target then set the follow flag to True
            if utils.distance(self.pos.x, self.pos.y, self.target.pos.x + 500, self.target.pos.y + 32) < 1000:
                self.follow = True

        elif utils.distance(self.pos.x, self.pos.y, self.target.pos.x - 500, self.target.pos.y + 32) < 1000:
            self.follow = True

        # If the missile is following the target
        if self.follow:
            # play the missile sound effect
            sounds.play("missile")
            # move the missile towards the current target
            self.moveTo(self.randomTargets[self.currentTarget])

            # if the missile is close enough to the current target set the next target as the current target
            if self.currentTarget < 2 and \
                        utils.distance(self.pos.x, self.pos.y, self.randomTargets[self.currentTarget].x, self.randomTargets[self.currentTarget].y ) < 100:
                self.currentTarget += 1


        # Update the missile's position, animation, and rotation.
        super().update()
        self.animSheet.play()
        self.rotate()

        # Check if the missile should be destroyed.
        # increment the missile's lifespan counter
        self.deathTime += utils.deltaTime()
        # if the missile has been alive for more than 100 milliseconds destroy it.
        if self.deathTime >= 100:
            self.destroy = True

        # if the missile has gone off the bottom of the screen destroy it.
        if self.pos.y >= 2000:
            self.destroy = True

    # Move the missile towards the given target using steering behavior.
    def moveTo(self,target):
        maxVel = 1000000 # maximum velocity the missile can have
        maxForce = 1.5   # maximum force that can be applied to the missile
        maxSpeed = 15    # maximum speed of the missile

        # Calculate the normalized direction vector from the missile's current position to the target position
        nor = Vector2(target.x - self.pos.x, target.y - self.pos.y).normalize()
        
        # Calculate the desired velocity, steering force, and apply the steering force to the missile's velocity
        desired_velocity = Vector2(nor.x * maxVel, nor.y * maxVel)
        
        # Calculate the steering force that needs to be applied to reach the desired velocity
        steering = Vector2(desired_velocity.x - self.vel.x, desired_velocity.y - self.vel.y)
        steering.scale_to_length(maxForce)
        
        # Update the missile's velocity by adding the steering force to it and scaling it to the maximum speed
        self.vel = Vector2(self.vel.x + steering.x, self.vel.y + steering.y)
        self.vel.scale_to_length(maxSpeed)
        
        # Update the missile's position based on its velocity
        self.pos.x = self.pos.x + self.vel.x
        self.pos.y = self.pos.y + self.vel.y


    # Create and return two mini projectiles with the missile's velocity and type.  
    def getProjectiles(self):
        p1 = MiniProjectile(self.pos, self.type)
        p2 = MiniProjectile(self.pos, self.type)

        p1.vel = self.vel
        p2.vel = self.vel

        p1.applyForce(Vector2(-5, 0))
        p2.applyForce(Vector2(5, 0))

        # Return the two mini projectiles
        return p1, p2


    def rotate(self):
        # Calculate the angle of the missile based on its velocity
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        a = angle
        angle += 0
        self.angle = angle

    def draw(self):
        # Set the offset of the rotated image to (0, 0)
        offset = Vector2(0, 0)
        # Rotate the missile's image based on its angle and update the missile's image
        rotated_image, rect = utils.rotate(self.animSheet.getCurrentFrame(), self.angle, [self.pos.x, self.pos.y],offset)
        self.img = rotated_image
        super().draw()

    def setTarget(self,target):
        # Set the missile's target to the given target
        self.target = target
        # Add three random targets to the missile's list of random targets
        self.randomTargets.append(Vector2(target.pos.x + random.randrange(-200,300),target.pos.y - 700))
        self.randomTargets.append(Vector2(target.pos.x + random.randrange(-200,300),target.pos.y - 900))
        self.randomTargets.append(Vector2(self.target.pos.x + 32, self.target.pos.y + 32))
        # Set the missile's current target index to 0
        self.currentTarget = 0