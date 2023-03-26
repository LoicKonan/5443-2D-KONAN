import pygame

class AssetsManager:
    def __init__(self):
        # Dictionary of assets, where the key is a string representing the name of the asset,
        # and the value is the loaded image file with transparency
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
        # Retrieve the image with the specified key from the dictionary
        return self.assets[key]


# New instance of the AssetsManager class to manage game assets
assetsManager = AssetsManager()
