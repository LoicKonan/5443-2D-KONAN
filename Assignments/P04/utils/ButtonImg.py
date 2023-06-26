import pygame

from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class ButtonImg:
    def __init__(self,id, pos,text, scale,img,clickImg,font = utils.font32):
        self.id = id
        self.text = text
        self.font = font

        self.img = img
        self.clickImg = clickImg
        self.drawImg = self.img
        self.pos = pos


        width = self.img.get_width()
        height = self.img.get_height()

        self.img = pygame.transform.scale(self.img, (int(width * scale.x), int(height * scale.y)))
        self.clickImg = pygame.transform.scale(self.clickImg, (int(width * scale.x), int(height * scale.y)))

        self.drawImg = self.img
        self.rect = self.drawImg.get_rect()
        self.rect.topleft = (pos.x,pos.y)
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.drawImg = self.clickImg
                action = True
                sounds.play("click")

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            self.drawImg = self.img

        # draw button on screen
        if self.clicked:
            self.rect.y = self.pos.y + 4
        else:
            self.rect.y = self.pos.y
        utils.screen.blit(self.drawImg, self.rect)

        if self.text != "":
            textT = self.font.render(self.text, True, (255,211,12))
            text_rect = textT.get_rect(center=(self.pos.x + self.drawImg.get_width() / 2, self.pos.y + self.drawImg.get_height() - textT.get_height()/2 ))
            text_rect.y += 10
            if self.clicked:
                text_rect.y += 4
            utils.screen.blit(textT, text_rect)

        return
