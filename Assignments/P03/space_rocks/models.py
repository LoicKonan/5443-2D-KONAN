import math
import random

import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom

from MUtils import mUtils
from messenger import Messenger
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, print_text

UP = Vector2(0, -1)



# Animate images in a list of images
image_paths = ["sprites/Portal/portal01.png", "sprites/Portal/portal02.png",
               "sprites/Portal/portal03.png", "sprites/Portal/portal04.png",
               "sprites/Portal/portal05.png", "sprites/Portal/portal06.png",
               "sprites/Portal/portal07.png", "sprites/Portal/portal08.png",
               "sprites/Portal/portal09.png", "sprites/Portal/portal10.png",
               "sprites/Portal/portal11.png", "sprites/Portal/portal12.png",
               "sprites/Portal/portal13.png", "sprites/Portal/portal14.png",
               "sprites/Portal/portal15.png", "sprites/Portal/portal16.png",
               "sprites/Portal/portal17.png", "sprites/Portal/portal18.png",
               "sprites/Portal/portal19.png", "sprites/Portal/portal20.png",
               "sprites/Portal/portal21.png", "sprites/Portal/portal22.png",
               "sprites/Portal/portal23.png", "sprites/Portal/portal24.png",
               "sprites/Portal/portal25.png", "sprites/Portal/portal26.png",
               "sprites/Portal/portal27.png", "sprites/Portal/portal28.png",
               "sprites/Portal/portal29.png", "sprites/Portal/portal30.png",
               "sprites/Portal/portal31.png", "sprites/Portal/portal32.png",
               "sprites/Portal/portal33.png", "sprites/Portal/portal34.png",
               "sprites/Portal/portal35.png", "sprites/Portal/portal36.png",
               "sprites/Portal/portal37.png", "sprites/Portal/portal38.png",
               "sprites/Portal/portal39.png", "sprites/Portal/portal40.png",
               "sprites/Portal/portal41.png", "sprites/Portal/portal42.png",
               "sprites/Portal/portal43.png", "sprites/Portal/portal44.png",
               "sprites/Portal/portal45.png", "sprites/Portal/portal46.png",
               "sprites/Portal/portal47.png", "sprites/Portal/portal48.png",
               "sprites/Portal/portal49.png", "sprites/Portal/portal50.png",
               "sprites/Portal/portal51.png", "sprites/Portal/portal52.png",
               "sprites/Portal/portal53.png", "sprites/Portal/portal54.png",
               "sprites/Portal/portal55.png", "sprites/Portal/portal56.png",
               "sprites/Portal/portal57.png", "sprites/Portal/portal58.png",
               "sprites/Portal/portal59.png", "sprites/Portal/portal60.png",
               "sprites/Portal/portal61.png", "sprites/Portal/portal62.png",
               "sprites/Portal/portal63.png", "sprites/Portal/portal64.png"]

current_image = 0
current_image_2 = 0



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

        textColor = (233, 23, 23) if self.creds is None else (23, 233, 23)
        mUtils.drawText(Vector2(self.position.x - 20, self.position.y - 20), str(self.health), textColor, 8)

        ###
        self.healthGeneTime -= mUtils.deltaTime()
        if self.healthGeneTime < 0:
            self.healthGeneTime = 60
            self.health += 10
            self.health = min(self.health, 100)
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

        self.size = max(self.size, 1)
        self.damage = max(self.damage, 1)
        
        sprite = pygame.transform.scale(self.sprite,(int(self.size),int(self.size)))
        blit_position = Vector2(self.position.x - 5,self.position.y - 5)
        surface.blit(sprite, blit_position)
        
        
        
        
class Wormhole(GameObject):

    def __init__(self,  screen, image_paths = image_paths):
        # Load images as surfaces
        images = [pygame.image.load(path).convert_alpha() for path in image_paths]

        # Create sprite object and set initial image
        sprite = pygame.sprite.Sprite()
        sprite.image = images[0]
        sprite.rect = sprite.image.get_rect()
        self.countRandTime = 0
        self.countAvailableTime = 0
        self.available = True


        self.screen = screen
        self.pos1 = Vector2(random.randrange(0, 800 - 200), random.randrange(0, 600 - 150))
        self.pos2 = Vector2(random.randrange(0, 800 - 200), random.randrange(0, 600 - 150))

        while self.pos1.distance_to(self.pos2) < 300:
            self.pos2 = Vector2(random.randrange(0, 800 - 200), random.randrange(0, 600 - 150))

        self.radius = 40
       

    def drawHole(self,pos):
        global current_image
        current_image_path = image_paths[current_image]
        current_image_surface = pygame.image.load(current_image_path)
        current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        blitPos = pos - Vector2(self.radius)
        self.screen.blit(current_image_surface,blitPos)


        current_image += 1
        if current_image >= len(image_paths):
            current_image = 0

    def randomPos(self):
        self.countRandTime = 0
        self.pos1 = Vector2(random.randrange(0, 800 - 200), random.randrange(0, 600 - 150))
        self.pos2 = Vector2(random.randrange(0, 800 - 200), random.randrange(0, 600 - 150))

        while self.pos1.distance_to(self.pos2) < 300:
            self.pos2 = Vector2(random.randrange(0, 800 - 200), random.randrange(0, 600 - 150))

    def update(self):
        if not self.available:
            self.countAvailableTime += 0.016
            if self.countAvailableTime >= 3:
                self.countAvailableTime = 0
                self.available = True
                self.randomPos()

    def draw(self, surface):
        if self.available:
            self.drawHole(self.pos1)
            self.drawHole(self.pos2)


        # pass
