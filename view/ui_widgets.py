from pygame.locals import *
import pygame as pg
from abc import abstractmethod
from logic.tile import Tile
import numpy as np
from logic.const import FEATURE_TYPES
from view.const import COLORS


class UIWidget(object):
    def __init__(self, parent: "Scene", pos: tuple[int, int]):
        self.parent = parent
        self.pos = pos

    @abstractmethod
    def draw(self):
        pass

    def get_screen(self):
        return self.parent.parent.parent.screen

    def on_resize(self):
        pass


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

    def update_tile(self, new_tile: Tile, pos: tuple[int, int]):
        self.board[pos] = TileWidget(new_tile, pos, self.tile_size, self)

    def draw(self):
        for tile in self.board.values():
            tile.draw()

    def on_resize(self):
        for tile in self.board.values():
            tile.on_resize()


class TileWidget(UIWidget):
    def __init__(self, tile, pos, size, parent):
        super().__init__(parent, (pos[0] * size - size / 2, pos[1] * size - size / 2))
        self.tile = tile
        self.tile_size = size
        self.coords = pos
        self.img = pg.Surface((size, size))
        self.img.fill(COLORS.FARM)
        self.rect = self.img.get_rect()
        self.render()
        self.on_resize()

    def _connection_pos(self, conn):
        number = conn.to_number()
        return [
            (x * self.tile_size, y * self.tile_size)
            for (x, y) in [
                (0, 1),
                (0, 1 / 2),
                (0, 0),
                (0, 0),
                (1 / 2, 0),
                (1, 0),
                (1, 0),
                (1, 1 / 2),
                (1, 1),
                (1, 1),
                (1 / 2, 1),
                (0, 1),
            ]
        ][number]

    def render(self):
        for feature in self.tile.features:
            conns = feature.connections
            points = []
            middle_point = (self.tile_size / 2, self.tile_size / 2)
            if len(conns) > 0:
                points = [self._connection_pos(c) for c in conns]
            if feature.type == FEATURE_TYPES.CLOISTER:
                pg.draw.circle(
                    self.img, COLORS.CLOISTER, middle_point, self.tile_size / 4, 0
                )
            elif (
                feature.type == FEATURE_TYPES.CITY
                or feature.type == FEATURE_TYPES.PENNANT_CITY
            ):
                additional_point = tuple(np.average([*points, middle_point], axis=0))

                if additional_point != middle_point:
                    points.append(additional_point)
                else:
                    if len(points) == 6:
                        points.insert(
                            3, np.average([points[2], points[3], middle_point], axis=0)
                        )
                        points.append(
                            np.average([points[6], points[0], middle_point], axis=0)
                        )

                col = COLORS.CITY
                if feature.type == FEATURE_TYPES.PENNANT_CITY:
                    col = COLORS.PENNANT_CITY
                pg.draw.polygon(self.img, col, points, 0)
            elif feature.type == FEATURE_TYPES.ROAD:
                if len(points) == 1:
                    points.append(middle_point)

                pg.draw.line(self.img, COLORS.ROAD, points[0], points[1], 5)
            elif feature.type == FEATURE_TYPES.FARM:
                pass  # already the background
            else:
                raise ValueError("Incorrect feature type")

    def draw(self):
        self.get_screen().blit(self.img, self.pos)

    def on_resize(self):
        x, y = self.get_screen().get_size()
        x /= 2
        y /= 2
        self.pos = (
            x + self.coords[0] * self.tile_size - self.tile_size / 2,
            y + self.coords[1] * self.tile_size - self.tile_size / 2,
        )
