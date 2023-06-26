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

from objects.Player import Player
from utils.util import utils


class GameManager:
    def __init__(self,addBulletCallBack,loadNextLevel):
        self.players = {}
        self.localPlayer = None
        self.loadNextLevel = loadNextLevel
        self.addBulletCallBack = addBulletCallBack
        self.sprites = pygame.sprite.Group()

    def addPlayer(self, id, player, localPlayer=False):
        """Adds a player to the local game as dictated by incoming messages."""

        # we don't want to try and manage the local player instance
        if localPlayer:
            self.localPlayer = player.id
        else:
            player = Player(id, None, None, Vector2(200, 400),self.addBulletCallBack)
            self.players[id] = player

    def update(self):

        for id, player in self.players.items():
            if player.destroyFlag:
                self.players.pop(id)
                break

    def draw(self):
        for id, player in self.players.items():
            player.draw()

    def callBack(self, ch, method, properties, body):
        # print(body)
        # try:
        #     b = body['sender']
        # except:
        #     print("error")
        #     return

        game = method.exchange  # not used here but passed in by pika
        exchange = method.exchange  # not used here but passed in by pika
        body = json.loads(body.decode("utf-8"))  # where all the game commands are
        data = body.get("data", None)
        sender = body["sender"]
        pos = data.get("pos", None)
        vel = data.get("vel", None)
        acc = data.get("acc", None)
        flipX = data.get("flipX", None)
        shoot = data.get("shoot", None)
        shootUp = data.get("shootUp", None)
        health = data.get("health", None)
        currentSheet = data.get("currentSheet", None)
        jumping = data.get("jumping", None)
        level = data.get("level", None)

        if self.localPlayer != sender:
            if not sender in self.players:
                self.addPlayer(sender, None)
                print(f"Players: {len(self.players)}")
            else:
                if pos:
                    self.players[sender].pos.x = pos[0]
                    self.players[sender].pos.y = pos[1]
                if vel:
                    self.players[sender].vel.x = vel[0]
                    self.players[sender].vel.y = vel[1]
                if acc:
                    self.players[sender].acc.x = acc[0]
                    self.players[sender].acc.y = acc[1]
                if flipX is not None:
                    self.players[sender].flipX = flipX
                if shoot:
                    self.players[sender].shoot()
                if shootUp is not None:
                    self.players[sender].shootUp = shootUp
                if health:
                    self.players[sender].health = health
                if currentSheet is not None:
                    self.players[sender].currentSheet = currentSheet
                if jumping is not None:
                    self.players[sender].jumping = jumping
                if level is not None:
                    if utils.currentLevel != level:
                        utils.currentLevel = level -1
                        self.loadNextLevel()

