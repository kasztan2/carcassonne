from abc import abstractmethod
from pygame.locals import *
import pygame as pg


# https://pygame.readthedocs.io/en/latest/5_app/app.html#add-the-text-class
class TextWidget(object):
    def __init__(
        self,
        parent: "GameView",
        text: str,
        fontsize: int,
        pos: tuple[int, int],
        color: tuple[int, int, int],
    ):
        self.parent = parent
        self.pos = pos
        self.font = pg.font.Font(None, fontsize)
        self.img = self.font.render(text, True, color)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        self.parent.screen.blit(self.img, self.rect)


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
