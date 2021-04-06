import pygame as pg
from .GameManager import GameManager
from .Input import Input
from .Screen import Screen
from .UI.UIManager import UIManager


class Renderer:
    def __init__(self):
        self.gm = GameManager()
        self.screen = Screen.screen()
        self.screen_size = Screen.screen_size()
        self.inp = Input()

        self.ui_manager = UIManager()

        self.blank_surface = pg.Surface(Screen.screen_size())
        self.blank_surface.fill(pg.Color(40, 40, 40))

        self.running = True
        self.just_loaded = False
        self.loaded = False

    def run(self):
        dirties = []
        self.clear()
        self.update()
        dirties.extend(self.draw())
        dirties.extend(self.post_draw())
        return dirties

    def exit(self):
        self.gm.exit()

    def clear(self):
        pass

    def fill(self):
        pass

    def update(self):
        pass

    def draw(self):
        return []

    def post_draw(self):
        return []

    def load(self):
        self.loaded = True
        self.just_loaded = True

    def unload(self):
        self.loaded = False
