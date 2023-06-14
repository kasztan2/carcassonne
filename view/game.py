import pygame as pg
from pygame.locals import *
from view.scenes import WelcomeScene


# singleton magic from stackoverflow: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GameView(object, metaclass=Singleton):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 800), RESIZABLE)
        self.running = True
        self.scenes = [WelcomeScene(self)]
        self.scene = self.scenes[0]

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False

            self.scene.draw()

            pg.display.update()

        pg.quit()
