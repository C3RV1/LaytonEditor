import PygameEngine.GameManager
import pygame as pg
import PygameEngine.Sprite
import PygameEngine.Camera
import PygameEngine.Input
import PygameEngine.Screen
import PygameEngine.Animation


class Renderer:
    def __init__(self):
        self.gm = PygameEngine.GameManager.GameManager()
        self.screen = PygameEngine.Screen.Screen.screen()
        self.screen_size = PygameEngine.Screen.Screen.screen_size()
        self.inp = PygameEngine.Input.Input()

        self.blank_surface = pg.Surface(PygameEngine.Screen.Screen.screen_size())
        self.blank_surface.fill(pg.Color(40, 40, 40))

        self.running = True
        self.first_clear = False

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
        return []

    def draw(self):
        return []

    def post_draw(self):
        return []

    def load(self):
        pass

    def unload(self):
        pass
