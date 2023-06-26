import pygame
from pygame.math import Vector2

from multiplayer.messenger import Messenger
from objects.Enemy.Enemy import Enemy
from objects.GameObject import GameObject
from objects.HealthBar import HealthBar
from objects.Projectile.PlayerProjectile1 import PlayerProjectile
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class Player(GameObject):
    def __init__(self, id, creds, callBack, pos, addBulletsCallBack):
        super().__init__(pos, None)

        self.addBulletsCallBack = addBulletsCallBack

        self.creds = creds
        self.callback = callBack
        self.id = id
        if self.creds is not None:
            self.messenger = Messenger(self.creds, self.callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 0.2

        self.sheets = {
            'idle': SpriteSheet(assetsManager.get("player"), 5, 12),
            'run': SpriteSheet(assetsManager.get("player"), 5, 12),
            'jump': SpriteSheet(assetsManager.get("player"), 5, 12),
            'shoot': SpriteSheet(assetsManager.get("player"), 5, 12),
            'shootUp': SpriteSheet(assetsManager.get("player"), 5, 12)
        }
        self.sheets['idle'].setPlay(0, 3, 0.07, True)
        self.sheets['run'].setPlay(12, 23, 0.07, True)
        self.sheets['jump'].setPlay(24, 24, 0.07, True)
        self.sheets['shoot'].setPlay(36, 39, 0.07, False)
        self.sheets['shootUp'].setPlay(48, 51, 0.07, False)

        self.currentSheet = 'idle'
        self.img = self.sheets[self.currentSheet].getCurrentFrame()
        self.prevPos = None
        self.speed = 5
        self.jumping = False
        self.shootUp = False
        self.health = 10
        self.healthBar = HealthBar(self.health, (23, 233, 233), self.getRect().w + 2)
        self.bullets = 0

    def update(self):
        self.applyForce(pygame.Vector2(0, 0.52))

        if self.currentSheet == 'shoot':
            if self.sheets[self.currentSheet].current >= 39:
                self.currentSheet = 'idle'
        elif self.currentSheet == 'shootUp':
            if self.sheets[self.currentSheet].current >= 51:
                self.currentSheet = 'idle'
        elif self.jumping:
            self.currentSheet = 'jump'
        elif self.vel.x != 0:
            self.currentSheet = 'run'
        else:
            self.currentSheet = 'idle'

        self.prevPos = Vector2(self.pos.x, self.pos.y)
        super().update()

        self.sheets[self.currentSheet].play()
        self.img = self.sheets[self.currentSheet].getCurrentFrame()

        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > 1000 and self.pos.x < 1280:
            self.destroyFlag = True

    def hit(self, obj):
        if isinstance(obj,Enemy):
            self.applyForce(Vector2(-5, -5))
        super().hit(obj)

    def draw(self):
        super().draw()
        self.healthBar.draw(self.health, Vector2(self.getRect().x, self.getRect().y - 12))

    def timeToBroadCast(self):
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )
            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    def updateData(self, shoot=False):
        self.broadcastData(
            {
                "pos": (self.pos.x, self.pos.y),
                "vel": (self.vel.x,self.vel.y),
                "acc": (self.acc.x, self.acc.y),
                "flipX": self.flipX,
                "shoot": shoot,
                "shootUp": self.shootUp,
                "health": self.health,
                'currentSheet': self.currentSheet,
                'jumping': self.jumping,
                "level": utils.currentLevel
            }
        )

    def shoot(self):
        projectile = None
        projectileSpeed = 12
        if self.shootUp:
            self.currentSheet = 'shootUp'
            self.sheets['shootUp'].setPlay(48, 51, 0.07, False)
            if not self.flipX:
                projectile = PlayerProjectile(Vector2(self.pos.x + 34, self.pos.y + 5), Vector2(0, -projectileSpeed),
                                              assetsManager.get("playerProjectileUp"))
            else:
                projectile = PlayerProjectile(Vector2(self.pos.x + 8, self.pos.y + 5), Vector2(0, -projectileSpeed),
                                              assetsManager.get("playerProjectileUp"))

        else:
            self.sheets['shoot'].setPlay(36, 39, 0.07, False)
            self.currentSheet = 'shoot'
            if not self.flipX:
                projectile = PlayerProjectile(Vector2(self.getCenter().x + 5, self.getCenter().y - 4),
                                              Vector2(projectileSpeed, 0),
                                              assetsManager.get("playerProjectile"))
            else:
                projectile = PlayerProjectile(Vector2(self.getCenter().x - 5, self.getCenter().y - 4),
                                              Vector2(-projectileSpeed, 0),
                                              assetsManager.get("playerProjectileLeft"))

        sounds.play("shoot")
        self.addBulletsCallBack(projectile)

    def onKeyDown(self, key):
        if key == pygame.K_a:
            self.flipX = True
            self.vel.x = -self.speed
            self.updateData()

        elif key == pygame.K_d:
            self.flipX = False
            self.vel.x = self.speed
            self.updateData()

        elif key == pygame.K_w:
            self.shootUp = True
            self.updateData()

        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -12))
            self.jumping = True
            self.updateData()

        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -12))
            self.jumping = True
            self.updateData()

        if key == pygame.K_UP:
            if self.bullets > 0:
                self.bullets -= 1
                self.shoot()
                self.updateData(True)

    def onKeyUp(self, key):
        if key == pygame.K_a and self.vel.x == -self.speed:
            self.vel.x = 0
            self.updateData()
        elif key == pygame.K_d and self.vel.x == self.speed:
            self.vel.x = 0
            self.updateData()
        elif key == pygame.K_w:
            self.shootUp = False
            self.updateData()

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x + 10, self.pos.y + 10, self.img.get_width() - 20, self.img.get_height() - 10)
        return rect
