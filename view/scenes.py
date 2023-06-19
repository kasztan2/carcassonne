from abc import abstractmethod
from pygame.locals import *
import pygame as pg
import pygame_gui as gui
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from view.ui_widgets import TextWidget, BoardWidget, InfoWidget
from view.utils import alignMousePosition, deCornify
from view.const import FONT_SIZE
from logic.game import CarcassonneGame
from logic.utils import Coords
import numpy as np
import traceback


class Scene:
    def __init__(self, parent, background_color):
        self.parent = parent
        self.background_color = background_color
        x, y = self.parent.screen.get_size()
        self.background = pg.Surface((x, y))
        self.background.fill(self.background_color)

        self.clear()

    def clear(self):
        x, y = self.parent.screen.get_size()
        self.parent.screen.blit(pg.transform.scale(self.background, (x, y)), (0, 0))

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def process_events(self, event):
        pass

    @abstractmethod
    def setup(self):
        pass


class WelcomeScene(Scene):
    def __init__(self, parent):
        super().__init__(parent, Color("chartreuse4"))
        self.welcomeText = TextWidget(
            self, "Welcome to the Carcassonne Game!", 50, (0, 0), (0, 0, 0)
        )

        self.label = gui.elements.UILabel(
            pg.rect.Rect(200, 100, 400, 100),
            "Enter the number of players (submit using enter)",
            self.parent.ui_manager,
        )
        self.label.set_text_scale(5)
        self.numberOfPlayers = UITextEntryLine(
            relative_rect=pg.rect.Rect(200, 200, 400, 50),
            manager=self.parent.ui_manager,
        )
        self.numberOfPlayers.set_allowed_characters("numbers")
        self.data = {"numPlayers": 0, "names": []}
        self.phase = 0

    def draw(self):
        self.welcomeText.draw()

        pg.display.flip()

    def validateNumber(self):
        if self.numberOfPlayers.get_text() == "":
            return False

        num = int(self.numberOfPlayers.get_text())
        if num >= 2 and num <= 5:
            return True

        return False

    def validateNames(self):
        names = []
        for field in self.nameInputs:
            names.append(field.get_text())

        if any(name == "" for name in names):
            return False

        if len(names) != len(set(names)):
            return False

        return True

    def process_events(self, event):
        if event.type == VIDEORESIZE:
            self.clear()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                if self.phase == 0:
                    if not self.validateNumber():
                        # TODO tell the user
                        return

                    self.data["numPlayers"] = int(self.numberOfPlayers.get_text())
                    self.phase = 1
                    self.numberOfPlayers.hide()
                    self.clear()
                    self.nameInputs = list(
                        map(
                            lambda x: UITextEntryLine(
                                relative_rect=pg.rect.Rect(200, 200 + 60 * x, 400, 50),
                                manager=self.parent.ui_manager,
                            ),
                            range(self.data["numPlayers"]),
                        )
                    )
                    self.label.set_text("Enter names:")
                else:
                    if not self.validateNames():
                        # TODO tell the user
                        return

                    self.data["names"] = [field.get_text() for field in self.nameInputs]
                    self.parent.game = CarcassonneGame.from_file_and_names(
                        "assets/default_tileset", self.data["names"]
                    )
                    for field in self.nameInputs:
                        field.hide()
                    self.label.hide()
                    self.parent.nextScene()

    def setup(self):
        self.clear()


class GameScene(Scene):
    def __init__(self, parent):
        super().__init__(parent, Color("blue"))
        self.board = BoardWidget(self, 200)
        self.boardZoom = 1.0
        self.meeplePointer = -1

        self.meeplePointerImage = pg.Surface((20, 20))
        self.turnPointer = pg.Surface((50, 50))
        self.turnPointer.fill(Color("blue"))
        pg.draw.polygon(self.turnPointer, Color("red"), [(10, 25), (40, 10), (40, 40)])

    def draw(self):
        if self.phase == 0:
            if self.info_widget.instruction_text != "Place a tile":
                self.clear()
                self.info_widget.instruction.clear_text_surface()
                self.info_widget.instruction.set_text("Place a tile")
                self.info_widget.instruction_text = "Place a tile"
        else:
            if self.info_widget.instruction_text != "Place a meeple":
                self.clear()
                self.info_widget.instruction.clear_text_surface()
                self.info_widget.instruction.set_text("Place a meeple")
                self.info_widget.instruction_text = "Place a meeple"

        self.board.draw()

        if self.phase == 1 and self.meeplePointer != -1:
            self.meeplePointerImage.fill(self.parent.game.get_current_player_color())
            self.parent.screen.blit(
                pg.transform.scale(
                    self.meeplePointerImage, (self.boardZoom * 20, self.boardZoom * 20)
                ),
                tuple(
                    map(
                        sum,
                        zip(
                            self.board.board[self.board.lastPos].pos,
                            np.array(
                                deCornify(
                                    self.board.board[self.board.lastPos].feature_points[
                                        self.meeplePointer
                                    ],
                                    self.board.tile_size,
                                )
                            )
                            * self.boardZoom,
                            (-10 * self.boardZoom, -10 * self.boardZoom),
                        ),
                    )
                ),
            )

        self.info_widget.draw()
        turn = self.parent.game.turn
        self.parent.screen.blit(self.turnPointer, ((200, 100 + turn * 50)))

    def setup(self):
        self.clear()
        self.board.update_tile(self.parent.game.board[Coords(0, 0)], (0, 0))
        self.phase = 0
        self.board.set_tile_to_place(self.parent.game.get_current_tile())

        self.info_widget = InfoWidget(self, self.parent.game.players)

    def handleEnd(self) -> bool:
        if not self.parent.game.is_finished():
            return False

        self.parent.game.handleEnd()
        self.info_widget.hide()
        self.parent.nextScene()
        return True

    def process_events(self, event):
        if event.type == VIDEORESIZE:
            self.clear()
            self.board.on_resize()
        elif event.type == MOUSEWHEEL:
            self.boardZoom += self.boardZoom * event.y * 0.1
            self.board.on_resize()
        elif event.type == MOUSEMOTION:
            if self.phase == 0 and self.board.tile_to_place is not None:
                self.board.tile_to_place.coords = alignMousePosition(
                    event.pos,
                    self.parent.screen.get_size(),
                    self.board._get_real_size(),
                )
                self.board.tile_to_place.on_resize()
        elif event.type == KEYDOWN:
            if event.key == K_r:
                if self.phase == 0 and self.board.tile_to_place is not None:
                    self.parent.game.tileset[-1].rotate(1)
                    self.board.tile_to_place.render()
                    self.clear()
            elif event.key == K_TAB:
                if self.phase == 1:
                    self.meeplePointer += 1
                    if self.meeplePointer == len(self.parent.game.lastTile.features):
                        self.meeplePointer = -1
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if self.phase == 0 and self.board.tile_to_place is not None:
                self.board.tile_to_place.coords = alignMousePosition(
                    event.pos,
                    self.parent.screen.get_size(),
                    self.board._get_real_size(),
                )

                try:
                    coords = self.board.tile_to_place.coords
                    self.parent.game.place_tile(self.board.tile_to_place.tile, coords)
                    self.board.update_tile(self.board.tile_to_place.tile, coords)
                    self.board.tile_to_place = None
                    self.phase = 1
                    self.meeplePointer = -1
                except Exception as e:
                    print("Can't place tile")
                    print(e)
                    traceback.print_exc()
            elif self.phase == 1:
                try:
                    self.parent.game.placeMeeple(self.meeplePointer)
                    tilesChanged = [x.coords for x in self.parent.game.tilesChanged]
                    for tile in tilesChanged:
                        self.board.board[tile.to_tuple()].render()
                    self.board.board[self.board.lastPos].render()
                    if self.handleEnd():
                        return
                    self.phase = 0
                    self.board.set_tile_to_place(self.parent.game.get_current_tile())
                except Exception as e:
                    print("Can't place meeple")
                    print(e)
                    traceback.print_exc()


class EndScene(Scene):
    def __init__(self, parent):
        super().__init__(parent, Color("gold"))
        self.top_label = None
        self.labels = []

    def setup(self):
        self.clear()
        self.top_label = gui.elements.UILabel(
            pg.Rect(200, 100, 400, 50), "Winner(s):", self.parent.ui_manager
        )

        winners = self.parent.game.get_winners()
        for i in range(len(winners)):
            self.labels.append(
                gui.elements.UILabel(
                    pg.Rect(200, 200 + i * 100, 400, 50),
                    f"{winners[i].name} with {winners[i].score} points",
                    self.parent.ui_manager,
                )
            )

    def draw(self):
        pass

    def process_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.parent.running = False
