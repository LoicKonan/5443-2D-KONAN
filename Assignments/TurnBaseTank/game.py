import pygame
from pygame import Vector2

from objects.Explosion import Explosion
from objects.Missile import Missile
from objects.Projectile import Projectile
from objects.Tank import Tank
from utils.map_generator import MapGenerator
from utils.sounds import Sounds, sounds
from utils.util import utils


class Game:
    def __init__(self):
        self.map = None
        self.winner = None
        self.currentTurn = None
        self.tank1 = None
        self.tank2 = None
        self.currentLevel = 0
        self.gameObjects = []
        self.velocity = 0.58
        self.currentProjectile = None

        self.newGame()


    def newGame(self):
        self.currentTurn = -1
        self.winner = None
        self.gameObjects = []
        self.map = MapGenerator()
        self.tank1 = Tank(Vector2(200, 100))
        self.tank2 = Tank(Vector2(1070, 100))
        self.gameObjects += self.map.gameObjects
        self.gameObjects.append(self.tank1)
        self.gameObjects.append(self.tank2)

        utils.camera.follow(None)

    def update(self):

        utils.camera.update()

        if self.currentTurn == -1:
            self.tank1.rotateCannon()
        else:
            self.tank2.rotateCannon()

        if self.tank1.pos.y > 2000:
            self.winner = 1
            return
        if self.tank2.pos.y > 2000:
            self.winner = -1
            return

        for object in self.gameObjects:
            object.update()

            if object.type == "tank" or object.type == "Projectile1" or object.type == "Projectile2":
                object.applyForce(Vector2(0, self.velocity))  # gravity

            if object.type == "tank":
                self.checkTankWithWall(object)

            if object.type == "Projectile1" or object.type == "Projectile2":
                self.checkProjectileCollision(object)
                if object.destroy:
                    self.gameObjects.remove(object)
                    utils.camera.follow(None)
                    self.gameObjects.append(Explosion(Vector2(object.pos.x - 32,object.pos.y - 32)))
                    sounds.play("explosion")

                    if isinstance(object, Projectile) or isinstance(object, Missile):
                        self.currentTurn *= -1
                    break

            if object.type == "Projectile1" and utils.collide(object,self.tank2) and self.tank2 is not None:
                self.winner = -1
                if self.gameObjects.__contains__(self.tank2):
                    self.gameObjects.remove(self.tank2)
                self.gameObjects.append(Explosion(self.tank2.pos))
                sounds.play("explosion")
                return

            if object.type == "Projectile2" and utils.collide(object,self.tank1) and self.tank1 is not None:
                self.winner = 1
                if self.gameObjects.__contains__(self.tank1):
                    self.gameObjects.remove(self.tank1)
                self.gameObjects.append(Explosion(self.tank1.pos))
                sounds.play("explosion")
                return

            if object.destroy and object.type == "wall":
                self.gameObjects.remove(object)

    def checkTankWithWall(self, tank):
        for otherObj in self.gameObjects:
            if utils.collide(tank, otherObj):
                if otherObj.type == "wall":
                    otherObj.onWallCollide(tank)

    def checkProjectileCollision(self,projectile):
        for otherObj in self.gameObjects:
            if utils.collide(projectile, otherObj):
                if otherObj.type == "wall":
                    otherObj.destroy = True
                    projectile.destroy = True

        if projectile.destroy:
            for otherObj in self.gameObjects:
                if otherObj.type == "wall" and utils.distance(projectile.pos.x,projectile.pos.y,otherObj.pos.x,otherObj.pos.y) < 50:
                    otherObj.destroy = True

    def onKeyDown(self, key):

        if self.winner is not None:
            if key == pygame.K_SPACE:
                self.newGame()
            return

        if key == pygame.K_w and self.currentProjectile is not None:
            p1, p2 = self.currentProjectile.getProjectiles()
            self.gameObjects.append(p1)
            self.gameObjects.append(p2)
            self.currentProjectile = None
            sounds.play("split")

        if utils.camera.target is not None:
            return
        if self.currentTurn == -1:
            self.tank1.onKeyDown(key)
        else:
            self.tank2.onKeyDown(key)

        if key == pygame.K_q:
            self.velocity -= 0.1
            if self.velocity < 0.1:
                self.velocity = 0.1
        elif key == pygame.K_e:
            self.velocity += 0.1
            if self.velocity > 1:
                self.velocity = 1




    def onKeyUp(self, key):
        if self.winner is not None:
            return

        if self.currentTurn == -1:
            self.tank1.onKeyUp(key)
        else:
            self.tank2.onKeyUp(key)

    def onMouseDown(self, event):
        if self.winner is not None:
            return

        if utils.camera.target is not None:
            return
        if self.currentTurn == -1:
            self.tank1.onMouseDown(event)
        else:
            self.tank2.onMouseDown(event)

    def onMouseUp(self, event):
        if self.winner is not None:
            return
        if utils.camera.target is not None:
            return

        if self.currentTurn == -1:
            self.tank1.onMouseUp(event)
            projectile = self.tank1.getProjectile()
            projectile.type = "Projectile1"
            self.gameObjects.append(projectile)
            utils.camera.follow(projectile)

            if isinstance(projectile,Projectile):
                self.currentProjectile = projectile
            elif isinstance(projectile,Missile):
                projectile.setTarget(self.tank2)
            sounds.play("projectile")

        else:
            self.tank2.onMouseUp(event)
            projectile = self.tank2.getProjectile()
            projectile.type = "Projectile2"
            self.gameObjects.append(projectile)
            utils.camera.follow(projectile)
            if isinstance(projectile, Projectile):
                self.currentProjectile = projectile
            elif isinstance(projectile, Missile):
                projectile.setTarget(self.tank1)
            sounds.play("projectile")

    def draw(self):
        utils.drawText(Vector2(10, 100), "gravity (Q-E): " + "{:.2f}".format(self.velocity) , (244, 244, 244), 24)
        utils.drawText(Vector2(10, 140), "A/D : move".format(self.velocity), (244, 244, 244), 24)
        utils.drawText(Vector2(10, 180), "hold mouse : shoot".format(self.velocity), (244, 244, 244), 24)
        utils.drawText(Vector2(10, 220), "(left : normal, right: missile)".format(self.velocity),(244, 244, 244), 24)
        utils.drawText(Vector2(10, 260), "W : special".format(self.velocity), (244, 244, 244), 24)
        for obj in self.gameObjects:
            # if utils.distance(obj.pos.x, obj.pos.y, 200, 500) < 50:
            #     continue

            utils.screen.blit(obj.img, (obj.pos.x - utils.camera.pos.x, obj.pos.y - utils.camera.pos.y))
            obj.draw()

        if self.winner == -1:
            utils.drawText(Vector2(500, 100), "Player 1 win!", (244, 23, 23), 43)
        elif self.winner == 1:
            utils.drawText(Vector2(500, 100), "Player 2 win!", (244, 23, 23), 43)

        if self.winner is not None:
            utils.drawText(Vector2(500, 140), "Press 'space' to restart!", (166, 23, 23), 32)
