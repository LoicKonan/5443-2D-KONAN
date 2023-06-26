import sys

import pygame
from pygame import Vector2

from Level.Level1 import Level1
from Level.Level2 import Level2
from Level.Level3 import Level3
from Level.Level4 import Level4
from Level.Level5 import Level5
from Level.Level6 import Level6
from multiplayer.comms import mykwargs
from multiplayer.manager import GameManager
from objects.Enemy.Enemy import Enemy
from objects.Explosion import Explosion
from objects.Player import Player
from objects.collectable.Bullets import Bullets
from objects.collectable.Potion import Potion
from objects.Projectile.EnemyProjectile import EnemyProjectile
from objects.Projectile.PlayerProjectile1 import PlayerProjectile
from objects.Projectile.Projectile import Projectile
from objects.Wall.Wall import Wall
from screens.Game import Game
from screens.GameOver import GameOver
from screens.YouWin import YouWin
from utils.util import utils





class MainGame(Game):
    def __init__(self):

        args, kwargs = mykwargs(sys.argv)

        queue = kwargs.get("queue", None)
        playerId = kwargs.get("player", None)
        creds = {
            "exchange": queue,
            "port": "5672",
            "host": "terrywgriffin.com",
            "user": playerId,
            "password": playerId + "2023!!!!!",
        }

        # set the window title
        pygame.display.set_caption(f"{creds['user']}")

        utils.currentLevel = 0

        utils.camera.y = 0
        utils.camera.x = 0
        self.levels = [Level1(),Level2(),Level3(),Level4(),Level5(),Level6()]
        self.gameObjects = self.levels[utils.currentLevel].gameObjects

        self.manager = GameManager(self.gameObjects.append,self.nextLevel)
        self.player = Player(playerId,creds,self.manager.callBack,self.levels[utils.currentLevel].playerPos,self.gameObjects.append)
        self.manager.addPlayer(playerId,self.player, True)
        self.gameObjects.append(self.player)

    def nextLevel(self):
        utils.currentLevel += 1
        if utils.currentLevel >= len(self.levels):
            utils.currentScreen = YouWin()
            return
        self.levels = [Level1(),Level2(),Level3(),Level4(),Level5(),Level6()]
        self.gameObjects = self.levels[utils.currentLevel].gameObjects
        for id, player in self.manager.players.items():
            if player.id != self.player.id:
                player.pos = self.levels[utils.currentLevel].playerPos
                player.addBulletsCallBack = self.gameObjects.append
        self.player.pos = self.levels[utils.currentLevel].playerPos
        self.gameObjects.append(self.player)
        self.player.addBulletsCallBack = self.gameObjects.append

    def update(self):
        if self.player.destroyFlag:
            utils.currentScreen = GameOver()

        utils.camera.x = self.player.pos.x - 400
        if utils.camera.x < 0:
            utils.camera.x = 0
        if utils.camera.x > 1280-800:
            utils.camera.x = 1280-800

        if self.player.pos.x > 1280:
            self.nextLevel()
            return

        objectsAdded = []

        for obj in self.gameObjects:
            obj.update()

            for otherObj in self.gameObjects:
                if isinstance(obj,Player):
                    if utils.collide(obj,otherObj):
                        if isinstance(otherObj,Wall):
                            otherObj.wallCollide(obj)
                        if isinstance(otherObj, Potion):
                            otherObj.destroyFlag = True
                            obj.health += 5
                        if isinstance(otherObj,Enemy):
                            obj.hit(otherObj)
                        if isinstance(otherObj, Bullets):
                            otherObj.destroyFlag = True
                            obj.bullets += 20


                if isinstance(obj, EnemyProjectile) and isinstance(otherObj, Player):
                    if utils.collide(obj, otherObj):
                        obj.destroyFlag = True
                        objectsAdded.append(Explosion(Vector2(obj.pos.x - 24, obj.pos.y - 24)))
                        otherObj.hit(obj)
                elif isinstance(obj,Projectile) and isinstance(otherObj,Wall):
                    if utils.collide(obj,otherObj):
                        obj.destroyFlag = True
                        objectsAdded.append(Explosion(Vector2(obj.pos.x - 24,obj.pos.y -24)))
                elif isinstance(obj,PlayerProjectile) and isinstance(otherObj,Enemy):
                    if utils.collide(obj,otherObj):
                        obj.destroyFlag = True
                        objectsAdded.append(Explosion(Vector2(obj.pos.x - 24, obj.pos.y - 24)))
                        otherObj.hit(obj)


        self.gameObjects += objectsAdded

        self.manager.update()
        minPlayerPosX = 99999
        for id, player in self.manager.players.items():
            if player.id != self.player.id:
                print(player.id)
                player.update()
                if player.pos.x < minPlayerPosX:
                    minPlayerPosX = player.pos.x
                for otherObj in self.gameObjects:
                    if isinstance(player, Player) :
                        if utils.collide(player, otherObj):
                            if isinstance(otherObj, Bullets):
                                otherObj.destroyFlag = True
                            elif isinstance(otherObj, Wall):
                                otherObj.wallCollide(player)

        if  utils.camera.x > minPlayerPosX - 400:
            utils.camera.x = minPlayerPosX - 400
        if self.player.pos.x > minPlayerPosX + 400 - 48:
            self.player.pos.x = minPlayerPosX + 400 - 48

        for obj in self.gameObjects:
            if obj.destroyFlag:
                self.gameObjects.remove(obj)

    def draw(self):
        self.levels[utils.currentLevel].draw()

        self.manager.draw()
        for obj in self.gameObjects:
            obj.draw()

        utils.drawText(Vector2(5, 580), "Bullets: " + str(self.player.bullets), (233, 233, 233), utils.font16)


    def onKeyDown(self, key):
        self.player.onKeyDown(key)

    def onKeyUp(self, key):
        self.player.onKeyUp(key)

    def onMouseDown(self, event):
        pass

    def onMouseUp(self, event):
        pass

    def onMouseWheel(self, event):
        pass

