from abc import abstractmethod
from pygame.locals import *
import pygame as pg
import pygame_gui as gui
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from view.ui_widgets import TextWidget


class Scene:
    def __init__(self, parent, background_color):
        self.parent = parent
        self.background_color = background_color

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def process_events(self, event):
        pass


class WelcomeScene(Scene):
    def __init__(self, parent):
        super().__init__(parent, Color("blue"))
        self.welcomeText = TextWidget(
            parent, "Welcome to the Carcassonne Game!", 50, (0, 0), (0, 0, 0)
        )

        self.parent.screen.fill(self.background_color)
        self.numberOfPlayers = UITextEntryLine(
            relative_rect=pg.rect.Rect(200, 200, 300, 300),
            manager=self.parent.ui_manager,
        )
        self.numberOfPlayers.set_allowed_characters("numbers")
        self.data = {"numPlayers": 0, "names": []}
        self.phase = 0

    def draw(self):
        self.welcomeText.draw()

        pg.display.flip()

    def validateNumber(self):
        print(self.numberOfPlayers.get_text())
        if self.numberOfPlayers.get_text() == "":
            return False

        num = int(self.numberOfPlayers.get_text())
        if num >= 2 and num <= 5:
            return True

        return False

    def process_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                if self.phase == 0:
                    if not self.validateNumber():
                        return

                    self.data["numPlayers"] = int(self.numberOfPlayers.get_text())
                    self.phase = 1
                    # del self.numberOfPlayers
                    print(self.data["numPlayers"])
                    self.parent.ui_manager.clear_and_reset()
