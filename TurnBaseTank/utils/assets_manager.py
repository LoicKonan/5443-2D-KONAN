import pygame


class AssetsManager:
    def __init__(self):
        self.assets = {
            'cell': pygame.image.load("assets/cell.png").convert_alpha(),
            'tank': pygame.image.load("assets/tank.png").convert_alpha(),
            'cannon': pygame.image.load("assets/cannon.png").convert_alpha(),
            'shootParticle': pygame.image.load("assets/shootParticle.png").convert_alpha(),
            'projectile': pygame.image.load("assets/projectile.png").convert_alpha(),
            'explo1': pygame.image.load("assets/explo1.png").convert_alpha(),
            'missile': pygame.image.load("assets/missile.png").convert_alpha()
        }

    def get(self, key):
        return self.assets[key]


assetsManager = AssetsManager()
