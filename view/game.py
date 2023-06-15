import pygame as pg
from pygame.locals import *
import pygame_gui as gui
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
        pg.display.set_caption("Carcassonne game")
        self.running = True

        self.clock = pg.time.Clock()
        self.ui_manager = gui.UIManager((800, 800))

        self.scenes = [WelcomeScene(self)]
        self.scene = self.scenes[0]

    def run(self):
        time_delta = self.clock.tick(60) / 1000.0
        while self.running:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False
                self.ui_manager.process_events(event)
                self.scene.process_events(event)

            self.ui_manager.update(time_delta)

            self.scene.draw()
            self.ui_manager.draw_ui(self.screen)

            pg.display.update()

        pg.quit()
