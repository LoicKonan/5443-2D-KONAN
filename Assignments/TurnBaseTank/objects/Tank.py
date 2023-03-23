import math

import pygame
from pygame import Vector2

from objects.Missile import Missile
from objects.Projectile import Projectile
from objects.gameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class Tank(GameObject):
    def __init__(self, pos):
        super().__init__(pos, assetsManager.get("tank"), "tank")
        self.speed = 1
        self.jumping = False
        self.flip = False
        self.cannonImg = assetsManager.get("cannon")
        self.angle = 0
        self.shotY = 7

        self.holding = False

        self.shootSheet = SpriteSheet(assetsManager.get("shootParticle"), 7, 5)
        self.shootSheet.setPlay(0, 34, 0.001, True)
        self.shootSheetPos = Vector2(0, 0)
        self.particleScale = 10

        self.projectilePos = Vector2(0,0)

        self.shootDir = Vector2(0, 0)
        self.projectileSpeed = 1
        self.isMissie = False

    def draw(self):

        cannonX = self.pos.x - 67
        cannonY = self.pos.y + self.shotY
        offset = Vector2(0, -20)
        rotated_image, rect = utils.rotate(self.cannonImg, self.angle, [cannonX, cannonY], offset)

        # self.shootSheetPos = Vector2(rect.x + rect.w,rect.y - rect.h )

        if self.shootSheetPos is not None:
            self.shootSheetPos = Vector2(rect.x, rect.y) + self.shootDir * 26

        rect.x -= utils.camera.pos.x - 100
        rect.y -= utils.camera.pos.y
        utils.screen.blit(rotated_image, rect)
        super().draw()

        if self.holding:
            sounds.play("hold")
            self.shotY += 0.2
            if self.shotY >= 10:
                self.shotY = 7

            # speed
            self.projectileSpeed += 0.15
            if self.projectileSpeed >= 30:
                self.projectileSpeed = 30

            # ball scale
            self.particleScale += 0.2
            if self.particleScale > 50:
                self.particleScale = 50

            self.shootSheet.play()
            particleImg = pygame.transform.scale(self.shootSheet.getCurrentFrame(), (self.particleScale, self.particleScale))
            self.shootSheetPos.x += 15
            self.shootSheetPos.y += 15

            self.shootSheetPos.x -= self.particleScale / 2
            self.shootSheetPos.y -= self.particleScale / 2
            self.projectilePos = Vector2(self.pos.x + 20,self.pos.y)

            utils.screen.blit(particleImg, (self.shootSheetPos.x - utils.camera.pos.x + 100,self.shootSheetPos.y- utils.camera.pos.y ))

    def rotateCannon(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        cannonX = self.pos.x - 67
        cannonY = self.pos.y + self.shotY

        dirX = mouseX - cannonX
        dirY = mouseY - cannonY
        angle = math.degrees(math.atan2(dirY, dirX))
        a = angle
        angle += 90
        if angle < -70:
            angle = -70
        elif angle > 70:
            angle = 70

        if a + 90 < -70:
            a = -70 - 90
        elif a + 90 > 70:
            a = 70 - 90

        self.angle = angle
        self.shootDir = Vector2(math.cos(math.radians(a)), math.sin(math.radians(a))).normalize()

    def onMouseDown(self, event):
        if event.button == 1:
            self.isMissie = False
        else:
            self.isMissie = True
        self.vel = Vector2(0, 0)
        self.holding = True
        self.projectileSpeed = 5
        pass

    def onMouseUp(self, event):
        self.shotY = 7
        self.holding = False
        self.particleScale = 10

    def getProjectile(self):
        force = self.shootDir * self.projectileSpeed
        if self.isMissie:
            projectile = Missile(self.projectilePos,force,"Projectile1")
        else:
            projectile = Projectile(self.projectilePos, force, "Projectile1")
        return projectile

    def onKeyUp(self, keycode):
        if keycode == pygame.K_a:
            if self.vel.x == -self.speed:
                self.vel.x = 0
        elif keycode == pygame.K_d:  #
            if self.vel.x == self.speed:
                self.vel.x = 0

    def onKeyDown(self, keycode):
        if keycode == pygame.K_a:  # press a move left
            if not self.flip:
                self.flip = True
            self.vel.x = -self.speed
        elif keycode == pygame.K_d:  # press d move right
            if self.flip:
                self.flip = False
            self.vel.x = self.speed
        elif keycode == pygame.K_SPACE:  # press space jump
            if not self.jumping:
                self.jumping = True
                self.pos.y -= 5
                self.applyForce(Vector2(0, -12.81))

    def setOnGround(self, onGround):
        self.jumping = False
