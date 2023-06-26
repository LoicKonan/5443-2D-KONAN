import pygame

from utils.util import utils


class HealthBar:
    def __init__(self,health,color,width):
        self.maxHealth = health
        self.color = color
        self.width = width

    def draw(self,health,pos):
        if health > 0 :
            maxHpWidth = self.width
            hpWidth = int(maxHpWidth / self.maxHealth)

            pygame.draw.rect(utils.screen, (233, 233, 233), (pos.x - utils.camera.x, pos.y - utils.camera.y, maxHpWidth, 4), 1)

            x = pos.x - utils.camera.x
            for i in range(0, health):
                pygame.draw.rect(utils.screen, self.color, (x, pos.y - utils.camera.y, hpWidth, 4))
                x += hpWidth