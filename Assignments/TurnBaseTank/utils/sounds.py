import pygame

class Sounds:
    def __init__(self):
        # Load sound effects
        self.ss = {
            'hold': pygame.mixer.Sound("assets/hold3.wav"),
            'projectile': pygame.mixer.Sound("assets/projectile2.wav"),
            'split': pygame.mixer.Sound("assets/split2.wav"),
            'explosion': pygame.mixer.Sound("assets/explosion.wav"),
            'missile': pygame.mixer.Sound("assets/missile.wav")
        }
        # Load and play background music
        pygame.mixer.music.load("assets/snowfall.ogg")
        pygame.mixer.music.play(-1)

    def play(self, key):
        # Stop specific sounds before playing new ones to prevent overlapping
        pygame.mixer.Sound.stop(self.ss['hold'])
        pygame.mixer.Sound.stop(self.ss['missile'])
        
        # Play sound based on key
        pygame.mixer.Sound.play(self.ss[key])

# Instantiate Sounds class
sounds = Sounds()
