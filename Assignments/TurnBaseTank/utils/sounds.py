import pygame




class Sounds:
    def __init__(self):
        self.ss = {
            'hold': pygame.mixer.Sound("assets/hold3.wav"),
            'projectile': pygame.mixer.Sound("assets/projectile2.wav"),
            'split': pygame.mixer.Sound("assets/split2.wav"),
            'explosion': pygame.mixer.Sound("assets/explosion.wav"),
            'missile': pygame.mixer.Sound("assets/missile.wav")
        }
        pygame.mixer.music.load("assets/snowfall.ogg")
        pygame.mixer.music.play(-1)

    def play(self, key):
        pygame.mixer.Sound.stop(self.ss['hold'])
        pygame.mixer.Sound.stop(self.ss['missile'])
        pygame.mixer.Sound.play(self.ss[key])


sounds = Sounds()
