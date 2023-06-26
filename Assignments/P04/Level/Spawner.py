from pygame import Vector2

from utils.util import utils


class Spawner:
    def __init__(self, addEnemyCallback):
        self.addEnemyCallback = addEnemyCallback
        self.timeBetween = 10
        self.time = 0
        self.countSpawnTime = 10

    def spawn(self):
        self.time += utils.deltaTime()
        self.countSpawnTime += utils.deltaTime()
        if self.countSpawnTime >= self.timeBetween:
            self.countSpawnTime = 0
