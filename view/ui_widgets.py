from pygame.locals import *
import pygame as pg
from abc import abstractmethod


class UIWidget(object):
    def __init__(self, parent: "GameView", pos: tuple[int, int]):
        self.parent = parent
        self.pos = pos

    @abstractmethod
    def draw(self):
        pass


# https://pygame.readthedocs.io/en/latest/5_app/app.html#add-the-text-class
class TextWidget(UIWidget):
    def __init__(
        self,
        parent: "GameView",
        text: str,
        fontsize: int,
        pos: tuple[int, int],
        color: tuple[int, int, int],
    ):
        super().__init__(parent, pos)
        self.font = pg.font.Font(None, fontsize)
        self.img = self.font.render(text, True, color)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        self.parent.screen.blit(self.img, self.rect)
