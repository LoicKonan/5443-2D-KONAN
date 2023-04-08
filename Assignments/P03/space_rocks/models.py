import math
import random

import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom

from MUtils import mUtils
from messenger import Messenger
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, print_text

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.destroy = False

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.10
    BULLET_SPEED = 10

    def __init__(self, position,spriteI,bulletSpriteI, create_bullet_callback, **kwargs):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")

        pygame.mixer.music.load("sound.mp3")
        pygame.mixer.music.play(-1)
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        self.creds = kwargs.get("creds", None)
        self.callback = kwargs.get("callback", None)
        self.id = kwargs.get("id", None)
        if self.creds is not None:
            self.messenger = Messenger(self.creds, self.callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 0

        self.healthGeneTime = 60
        self.health = 100
        self.score = 0
        self.thrustStop = 2
        self.activeBulletSkill = False
        self.bulletDamage = 10
        self.angle = 0

        if spriteI == None:
            self.spriteI = random.randrange(0, 10)
            self.bulletSpriteI = random.randrange(0, 4)
        else:
            self.spriteI = spriteI
            self.bulletSpriteI = bulletSpriteI

        super().__init__(position, load_sprite("space_ship" + str(self.spriteI)), Vector2(0))

    def timeToBroadCast(self):
        """check to see if there was enough delay to broadcast again"""
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )
            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self, dir):
        self.velocity += self.direction * self.ACCELERATION * dir

    def stop(self):
        if self.velocity.x != 0 and self.velocity.y != 0 and self.thrustStop > 0:
            self.thrustStop -= 1
            self.velocity = Vector2(0, 0)

    def draw(self, surface):
        self.angle = math.atan2(self.direction.y,self.direction.x) * 180 / math.pi
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite,  angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

        textColor = (23, 233, 23)
        if self.creds is None:
            textColor = (233, 23, 23)
        mUtils.drawText(Vector2(self.position.x - 20, self.position.y - 20), str(self.health), textColor, 8)

        ###
        self.healthGeneTime -= mUtils.deltaTime()
        if self.healthGeneTime < 0:
            self.healthGeneTime = 60
            self.health += 10
            if self.health >100:
                self.health = 100
            self.updateData()

        ## skill
        if self.score >= 5:
            self.activeBulletSkill = True
            self.bulletDamage = 20

    def updateData(self, scoreTo=None):
        self.broadcastData(
            {
                "pos": (self.position.x, self.position.y),
                "vel": (self.velocity.x, self.velocity.y),
                "dir": (self.direction.x, self.direction.y),
                "shoot": False,
                "health": self.health,
                "destroy": self.destroy,
                "scoreTo": scoreTo,
                "score": self.score,
                "spriteI":self.spriteI,
                "bulletSpriteI": self.bulletSpriteI,
                "bulletDamage": self.bulletDamage,
                "activeBulletSkill":self.activeBulletSkill,
                "angle": self.angle
            }
        )

    def sendShoot(self):
        self.broadcastData(
            {
                "pos": (self.position.x, self.position.y),
                "vel": (self.velocity.x, self.velocity.y),
                "dir": (self.direction.x, self.direction.y),
                "shoot": True,
                "health": self.health,
                "destroy": self.destroy,
                "activeBulletSkill":self.activeBulletSkill,
                "angle": self.angle
            }
        )

    def shoot(self,angle):
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))

        dir = Vector2(x,y)

        bullet_velocity = dir * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity, self.id,self.bulletSpriteI, self.bulletDamage )
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def getHit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy = True


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position, velocity, id,spriteI,damage):
        super().__init__(position, load_sprite("bullet" + str(spriteI)), velocity)
        self.id = id
        self.damage = 10
        self.size = 10

    def move(self, surface):
        self.position = self.position + self.velocity

    def draw(self, surface):
        self.size -= mUtils.deltaTime() * 6
        self.damage -= mUtils.deltaTime() * 6

        if self.size < 1:
            self.size = 1
        if self.damage < 1:
            self.damage = 1

        sprite = pygame.transform.scale(self.sprite,(int(self.size),int(self.size)))
        blit_position = Vector2(self.position.x - 5,self.position.y - 5)
        surface.blit(sprite, blit_position)