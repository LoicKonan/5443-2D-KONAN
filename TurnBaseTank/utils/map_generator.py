import random

from pygame import Vector2

from objects.gameObject import GameObject
from utils.assets_manager import assetsManager


class Platform:
    def __init__(self, pos, rows, cols):
        img = assetsManager.get("cell")
        tileSize = img.get_width()

        self.rows = rows
        self.cols = cols
        self.pos = pos
        self.gameObjects = []

        x = pos.x
        y = pos.y

        for row in range(0, rows):
            for col in range(0, cols):
                obj = GameObject(Vector2(x, y), img,"wall")
                self.gameObjects.append(obj)
                x += tileSize
            x = pos.x
            y += tileSize


class MapGenerator:
    def __init__(self):
        self.gameObjects = []
        self.platforms = []

        r = random.randrange(0,3)

        if r == 0:
            self.platforms.append( Platform(Vector2(50,650),20,100) )
            self.platforms.append(Platform(Vector2(1050, 650), 20, 100))
        elif r == 1:
            self.platforms.append(Platform(Vector2(50, 550), 20, 100))
            self.platforms.append(Platform(Vector2(1050, 550), 20, 100))
            self.platforms.append(Platform(Vector2(620, 450), 15, 15))
            self.platforms.append(Platform(Vector2(820, 500), 15, 15))
            self.platforms.append(Platform(Vector2(720, 250), 30, 30))
        elif r == 2:
            self.platforms.append(Platform(Vector2(50, 550), 2, 350))
            self.platforms.append(Platform(Vector2(50, 330), 2, 350))

        for platform in self.platforms:
            self.gameObjects += platform.gameObjects
