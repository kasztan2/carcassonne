from abc import abstractmethod
from pygame.locals import *
import pygame as pg
import pygame_gui as gui
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from view.ui_widgets import TextWidget, BoardWidget
from logic.game import CarcassonneGame
from logic.utils import Coords


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

    def draw(self):
        self.board.draw()

    def setup(self):
        self.clear()
        self.board.update_tile(self.parent.game.board[Coords(0, 0)], (0, 0))

    def process_events(self, event):
        if event.type == VIDEORESIZE:
            self.clear()
            self.board.on_resize()
        elif event.type == MOUSEWHEEL:
            self.boardZoom += self.boardZoom * event.y * 0.1
            self.board.on_resize()
