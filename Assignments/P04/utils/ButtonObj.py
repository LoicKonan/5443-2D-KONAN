import pygame

from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class ButtonObj:
    def __init__(self,id,obj):
        self.id = id
        self.obj = obj

        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.obj.getRect().collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                sounds.play("click")

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        pygame.draw.rect(utils.screen,(233,233,233),(self.obj.getRect().x,self.obj.getRect().y,self.obj.getRect().w,self.obj.getRect().h),1)
        self.obj.update()
        self.obj.draw()
