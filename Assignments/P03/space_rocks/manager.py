import pygame
from random import randint
import json
import sys
from rich import print
from threading import Thread
import math
import os
from pygame.math import Vector2

import pygame.display

# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender
from models import Spaceship


class GameManager:
    def __init__(self,create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.players = {}
        self.localPlayer = None
        self.sprites = pygame.sprite.Group()

    def addPlayer(self,spriteI,bulletSpriteI, **kwargs):
        """Adds a player to the local game as dictated by incoming messages."""
        name = kwargs.get("name", None)
        player = kwargs.get("player", None)
        localPlayer = kwargs.get("localPlayer", False)

        # we don't want to try and manage the local player instance
        if localPlayer:
            self.localPlayer = player.id
            self.spaceShip = player
        else:
            # this is a new player that needs just a basic player class
            # with no messaging capabilites. This is a mirror of another
            # player somewhere else.
            player = Spaceship((400,400),spriteI,bulletSpriteI,self.create_bullet_callback,id=name)
            self.players[name] = player

    def update(self,screen):
        for id, player in self.players.items():
            player.move(screen)

        for id, player in self.players.items():
            if player.destroy:
                self.players.pop(id)
                break


    def draw(self,screen):
        try:
            for id, player in self.players.items():
                player.draw(screen)
        except:
            pass

    def callBack(self, ch, method, properties, body):
        game = method.exchange  # not used here but passed in by pika
        exchange = method.exchange  # not used here but passed in by pika
        body = json.loads(body.decode("utf-8"))  # where all the game commands are
        data = body.get("data", None)
        sender = body["sender"]
        xy = data.get("pos", None)
        vel = data.get("vel", None)
        dir = data.get("dir", None)
        shoot = data.get("shoot", False)
        health = data.get("health", None)
        destroy = data.get("destroy", None)
        scoreTo = data.get("scoreTo", None)
        score = data.get("score", None)
        angle = data.get("angle",None)

        spriteI = data.get("spriteI", None)
        bulletSpriteI = data.get("bulletSpriteI", None)

        bulletDamage = data.get("bulletDamage", None)

        activeBulletSkill = data.get("activeBulletSkill",None)

        # if scoreTo is not None:
        #     print(scoreTo)
        #     print(self.players)

        if self.localPlayer != sender:
            #print(f"not local: {sender} != {self.localPlayer}")
            if not sender in self.players:
                self.addPlayer(spriteI,bulletSpriteI,name=sender)
                print(f"Players: {len(self.players)}")
            else:
                if xy:
                    self.players[sender].position.x = xy[0]
                    self.players[sender].position.y = xy[1]
                if vel:
                    self.players[sender].velocity.x = vel[0]
                    self.players[sender].velocity.y = vel[1]
                if dir:
                    self.players[sender].direction.x = dir[0]
                    self.players[sender].direction.y = dir[1]
                if activeBulletSkill:
                    self.players[sender].activeBulletSkill = self.players[sender].activeBulletSkill
                if angle:
                    self.players[sender].angle = angle
                if shoot is True:
                    self.players[sender].shoot(self.players[sender].angle)
                    if self.players[sender].activeBulletSkill:
                        self.players[sender].shoot(self.players[sender].angle - 5)
                        self.players[sender].shoot(self.players[sender].angle + 5)
                if health:
                    self.players[sender].health = health
                if destroy:
                    self.players[sender].destroy = destroy
                if scoreTo and scoreTo in self.players:
                    self.players[scoreTo].score += 1
                if scoreTo and scoreTo == self.spaceShip.id:
                    self.spaceShip.score += 1
                    self.spaceShip.updateData()
                if score:
                    self.players[sender].score = score
                if bulletDamage:
                    self.players[sender].bulletDamage = bulletDamage
        else:
            # print("local player")
            pass