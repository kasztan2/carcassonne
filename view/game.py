import pygame as pg
from pygame.locals import *
import pygame_gui as gui
from view.scenes import WelcomeScene, GameScene, EndScene


class GameView(object):
    """Manages the whole graphics of the game"""

    def __init__(self) -> None:
        self.game = None

        pg.init()
        self.screen = pg.display.set_mode((800, 800), RESIZABLE)
        pg.display.set_caption("Carcassonne game")
        self.running = True

        self.clock = pg.time.Clock()
        self.ui_manager = gui.UIManager((800, 800))

        self.scenes = [WelcomeScene(self), GameScene(self), EndScene(self)]
        self.scene = self.scenes[0]
        self.sceneIndex = 0
        self.scene.setup()

    def run(self) -> None:
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

    def nextScene(self) -> None:
        self.sceneIndex += 1
        if self.sceneIndex >= len(self.scenes):
            raise Exception("scene index out of range")
        self.scene = self.scenes[self.sceneIndex]
        self.scene.setup()
