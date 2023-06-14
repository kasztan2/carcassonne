from abc import abstractmethod
from pygame.locals import *
import pygame as pg
from view.ui_widgets import TextWidget


class Scene:
    def __init__(self, parent, background_color):
        self.parent = parent
        self.background_color = background_color

    @abstractmethod
    def draw(self):
        pass


class WelcomeScene(Scene):
    def __init__(self, parent):
        super().__init__(parent, Color("blue"))
        self.welcomeText = TextWidget(
            parent, "Welcome to the Carcassonne Game!", 50, (0, 0), (0, 0, 0)
        )

    def draw(self):
        self.parent.screen.fill(self.background_color)

        self.welcomeText.draw()

        pg.display.flip()
