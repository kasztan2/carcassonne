from pygame.locals import *
import pygame as pg
from abc import abstractmethod
from logic.tile import Tile


class UIWidget(object):
    def __init__(self, parent: "Scene", pos: tuple[int, int]):
        self.parent = parent
        self.pos = pos

    @abstractmethod
    def draw(self):
        pass

    def get_screen(self):
        return self.parent.parent.screen


# https://pygame.readthedocs.io/en/latest/5_app/app.html#add-the-text-class
class TextWidget(UIWidget):
    def __init__(
        self,
        parent: "Scene",
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
        self.parent.parent.screen.blit(self.img, self.rect)


class BoardWidget(UIWidget):
    def __init__(self, parent: "Scene", tile_size: int):
        super().__init__(parent, (0, 0))
        self.board = dict()
        self.tile_size = tile_size

    def update(self, new_tile: Tile, pos: tuple[int, int]):
        self.board[pos] = TileWidget(new_tile, pos, self.tile_size, self)

    def draw(self):
        for tile in self.board:
            tile.draw()


class TileWidget(UIWidget):
    def __init__(self, tile, pos, size, parent):
        super().__init__(parent, (pos[0] * size - size / 2, pos[1] * size - size / 2))
        self.tile = tile

    def draw(self):
        pass
