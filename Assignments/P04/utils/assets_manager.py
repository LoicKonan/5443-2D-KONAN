import pygame


class AssetsManager:
    def __init__(self):
        self.assets = {
            'button': pygame.image.load("assets/btn.png").convert_alpha(),
            'clickButton': pygame.image.load("assets/clickBtn.png").convert_alpha(),
            'bg': pygame.image.load("assets/Background.png").convert_alpha(),
            'player': pygame.image.load("assets/player.png").convert_alpha(),
            'wall': pygame.image.load("assets/wall.png").convert_alpha(),
            'playerProjectile': pygame.image.load("assets/playerProjectile.png").convert_alpha(),
            'playerProjectileUp': pygame.image.load("assets/playerProjectileUp.png").convert_alpha(),
            'playerProjectileLeft': pygame.image.load("assets/playerProjectileLeft.png").convert_alpha(),
            'explo1': pygame.image.load("assets/explo1.png").convert_alpha(),
            'enemy1': pygame.image.load("assets/enemy1.png").convert_alpha(),
            'enemy2': pygame.image.load("assets/enemy2.png").convert_alpha(),
            'movingWall': pygame.image.load("assets/movingWall.png").convert_alpha(),
            'enemyProjectile': pygame.image.load("assets/enemyProjectile.png").convert_alpha(),
            'enemyProjectile2': pygame.image.load("assets/enemyProjectile2.png").convert_alpha(),
            'hp': pygame.image.load("assets/hp.png").convert_alpha(),
            'enemy3': pygame.image.load("assets/enemy3.png").convert_alpha(),
            'bullets': pygame.image.load("assets/bullets.png").convert_alpha(),
        }

    def get(self, key):
        return self.assets[key]


assetsManager = AssetsManager()
