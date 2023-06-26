import pygame
from pygame.math import Vector2

from objects.Enemy.Enemy import Enemy
from objects.HealthBar import HealthBar
from objects.Projectile.EnemyProjectile import EnemyProjectile
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.util import utils


class Enemy2(Enemy):
    def __init__(self,pos,addProjectileCallback):
        super().__init__(pos)
        self.attackSpeed = SpriteSheet(assetsManager.get("enemy2"),1,6)
        self.attackSpeed.setPlay(0,5,0.3,True)
        self.addProjectileCallback = addProjectileCallback

        self.currentSheet = self.attackSpeed
        self.damage = 1
        self.health = 20
        self.img = self.currentSheet.getCurrentFrame()
        self.healthBar = HealthBar(self.health, (233, 23, 23), self.getRect().w + 4)


    def update(self):
        self.currentSheet.play()
        self.img = self.currentSheet.getCurrentFrame()
        self.shoot()

    def shoot(self):
        if self.currentSheet.current >= 4:
            self.currentSheet.current = 0
            p = EnemyProjectile(Vector2(self.getCenter().x,self.getCenter().y + 20),Vector2(-7,0),assetsManager.get("enemyProjectile"))
            self.addProjectileCallback(p)


    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x + 20, self.pos.y + 20, self.img.get_width() - 40, self.img.get_height()-40)
        return rect

    def draw(self):
        super().draw()
        self.healthBar.draw(self.health, Vector2(self.getRect().x, self.getRect().y - 12))
