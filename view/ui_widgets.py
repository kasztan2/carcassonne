from pygame.locals import *
import pygame as pg
from abc import abstractmethod
from logic.tile import Tile
import numpy as np
from logic.const import FEATURE_TYPES
from view.const import COLORS
from view.utils import deCornify
from copy import copy
import pygame_gui as gui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.scenes import Scene


class UIWidget(object):
    """Abstract class for custom UI widgets"""

    def __init__(self, parent: "Scene", pos: tuple[int, int]):
        self.parent = parent
        self.pos = pos

    @abstractmethod
    def draw(self):
        pass

    def get_screen(self):
        """Get the screen that this feature should be drawn on"""
        return self.parent.parent.parent.screen

    def on_resize(self):
        """Adjust to the new size of the screen"""
        pass


# https://pygame.readthedocs.io/en/latest/5_app/app.html#add-the-text-class
class TextWidget(UIWidget):
    """A redundant widget that can be replaced by pygame_gui's UILabel"""

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
    """Widget containing tiles on the board and handling the placing of tiles and meeples (basically coordinating the Tile widgets)"""

    def __init__(self, parent: "Scene", tile_size: int):
        super().__init__(parent, (0, 0))
        self.board = dict()
        self.tile_size = tile_size
        self.tile_to_place = None
        self.lastPos = (0, 0)

    def set_tile_to_place(self, tile_to_place):
        self.tile_to_place = TileWidget(tile_to_place, (0, 0), self.tile_size, self)

    def update_tile(self, new_tile: Tile, pos: tuple[int, int]):
        self.board[pos] = TileWidget(new_tile, pos, self.tile_size, self)
        self.lastPos = pos

    def draw(self):
        if self.tile_to_place is not None:
            self.parent.clear()

        for tile in self.board.values():
            tile.draw()

        if self.tile_to_place is not None:
            self.tile_to_place.draw()

    def on_resize(self):
        self.parent.clear()
        for tile in self.board.values():
            tile.on_resize()

    def _get_real_size(self):
        return self.parent.boardZoom * self.tile_size


class TileWidget(UIWidget):
    """Tile widget"""

    def __init__(self, tile, pos, size, parent):
        super().__init__(parent, (pos[0] * size - size / 2, pos[1] * size - size / 2))
        self.tile = tile
        self.tile_size = size
        self.coords = pos
        self.img = None
        self.rect = None
        self.feature_points = []
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
        """Draw the tile image and remember it"""
        self.img = pg.Surface((self.tile_size, self.tile_size))
        self.img.fill(COLORS.FARM)

        self.rect = self.img.get_rect()

        self.feature_points = []
        cloisterOnTile = any(
            [feature.type == FEATURE_TYPES.CLOISTER for feature in self.tile.features]
        )
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
                self.feature_points.append(copy(middle_point))
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

                self.feature_points.append(tuple(np.average(points, axis=0)))
            elif feature.type == FEATURE_TYPES.ROAD:
                if len(points) == 1:
                    points.append(middle_point)

                pg.draw.line(self.img, COLORS.ROAD, points[0], points[1], 5)

                self.feature_points.append(tuple(np.average(points, axis=0)))
            elif feature.type == FEATURE_TYPES.FARM:
                # already the green background
                if cloisterOnTile:
                    self.feature_points.append(
                        (1 / 4 * self.tile_size, 1 / 4 * self.tile_size)
                    )
                else:
                    self.feature_points.append(tuple(np.average(points, axis=0)))
            else:
                raise ValueError("Incorrect feature type")

            if feature.meeple is not None:
                meeple_pos = self.feature_points[-1]
                x, y = deCornify(meeple_pos, self.tile_size)
                pg.draw.rect(
                    self.img, feature.meeple.color, ((x - 10, y - 10), (20, 20))
                )

        print(f"Rendering tile done: {self.feature_points}")

    def _get_real_size(self):
        """Get the de facto size of the tile on screen (taking zoom into account)"""
        return self.parent.parent.boardZoom * self.tile_size

    def draw(self):
        realSize = self._get_real_size()
        self.get_screen().blit(
            pg.transform.scale(self.img, (realSize, realSize)), self.pos
        )

    def on_resize(self):
        x, y = self.get_screen().get_size()
        x /= 2
        y /= 2
        realSize = self._get_real_size()
        self.pos = (
            x + self.coords[0] * realSize - realSize / 2,
            y + self.coords[1] * realSize - realSize / 2,
        )


class InfoWidget(UIWidget):
    """Widget for displaying information about players"""

    def __init__(self, parent, players):
        super().__init__(parent, (0, 0))
        self.instruction = gui.elements.UILabel(
            pg.Rect(0, 0, 200, 50), "Place a tile", self.parent.parent.ui_manager
        )
        self.instruction.set_text_scale(2)
        self.instruction_text = "Place a tile"
        self.players = [
            PlayerWidget(self, players[i], (0, i * 50 + 100))
            for i in range(len(players))
        ]

    def draw(self):
        for player in self.players:
            player.draw()

    def hide(self):
        self.instruction.hide()
        for player in self.players:
            player.hide()


class PlayerWidget(UIWidget):
    """Widget for displaying information about a single player"""

    def __init__(self, parent, player, pos):
        super().__init__(parent, pos)
        self.name = player.name
        self.color = player.color
        self.player = player

        self.color_rect = None
        self.label = gui.elements.UILabel(
            pg.Rect(50, self.pos[1], 150, 50),
            f"{self.name} | {self.player.meeplesLeft} | {self.player.score}",
            self.parent.parent.parent.ui_manager,
        )
        self.label.set_text_scale(2)

        self.render()

    def set_label(self):
        self.label.set_text(
            f"{self.name} | {self.player.meeplesLeft} | {self.player.score}"
        )

    def render(self):
        self.color_rect = pg.Surface((50, 50))
        pg.draw.rect(self.color_rect, self.color, pg.Rect(0, 0, 50, 50))

    def draw(self):
        screen = self.get_screen()
        self.set_label()
        screen.blit(self.color_rect, (0, self.pos[1]))

    def hide(self):
        self.label.hide()
