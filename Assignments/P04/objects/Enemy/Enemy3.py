import pygame
from pygame.math import Vector2

from objects.Enemy.Enemy import Enemy
from objects.HealthBar import HealthBar
from objects.Projectile.EnemyProjectile import EnemyProjectile
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


class Enemy3(Enemy):
    def __init__(self,pos,dest,addProjectileCallback):
        super().__init__(pos)
        self.attackSpeed = SpriteSheet(assetsManager.get("enemy3"),1,5)
        self.attackSpeed.setPlay(0,4,0.07,True)
        self.addProjectileCallback = addProjectileCallback

        self.currentSheet = self.attackSpeed
        self.damage = 1
        self.health = 100
        self.img = self.currentSheet.getCurrentFrame()
        self.healthBar = HealthBar(self.health, (233, 23, 23), self.getRect().w + 45)

        self.start = Vector2(pos.x, pos.y)
        self.dest = dest
        self.speed = 2


    def update(self):
        self.currentSheet.play()
        self.img = self.currentSheet.getCurrentFrame()

        self.pos.x += self.speed
        if utils.distance(self.pos.x,self.pos.y,self.dest.x,self.dest.y) <= 10:
            tmp = Vector2(self.start.x,self.start.y)
            self.start = Vector2(self.dest.x,self.dest.y)
            self.dest = tmp
            self.speed *= -1

        if self.speed > 0:
            self.flipX = True
        else:
            self.flipX = False


        self.shoot()

    def shoot(self):
        if self.currentSheet.current >= 4:
            self.currentSheet.current = 0
            p = EnemyProjectile(Vector2(self.getCenter().x,self.getCenter().y + 20),Vector2(0,7),assetsManager.get("enemyProjectile2"))
            self.addProjectileCallback(p)


    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x + 20, self.pos.y + 20, self.img.get_width() - 40, self.img.get_height()-40)
        return rect

    def draw(self):
        super().draw()
        self.healthBar.draw(self.health, Vector2(self.getRect().x, self.getRect().y - 12))
