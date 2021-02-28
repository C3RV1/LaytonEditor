import PygameEngine.GameManager
import pygame as pg
import PygameEngine.Sprite
import PygameEngine.Camera
import PygameEngine.Input
import PygameEngine.Screen
import PygameEngine.Animation
from PygameEngine import Renderer


class TwoScreenRenderer(Renderer.Renderer):
    def __init__(self):
        super(TwoScreenRenderer, self).__init__()
        self.top_screen_group = pg.sprite.LayeredDirty()
        self.bottom_screen_group = pg.sprite.LayeredDirty()

        self.top_screen_camera = PygameEngine.Camera.Camera()
        self.top_screen_camera.display_port = pg.rect.Rect(0, 0, 256 * 2, 192 * 2)
        self.top_screen_camera.scale = 2

        self.bottom_screen_camera = PygameEngine.Camera.Camera()
        self.bottom_screen_camera.display_port = pg.rect.Rect(0, 192 * 2, 256 * 2, 192 * 2)
        self.bottom_screen_camera.scale = 2

        self.top_screen_group.set_clip(self.top_screen_camera.display_port)
        self.bottom_screen_group.set_clip(self.bottom_screen_camera.display_port)

        self.running = True

    def exit(self):
        self.gm.exit()

    def clear(self):
        self.top_screen_group.clear(self.screen, self.blank_surface)
        self.bottom_screen_group.clear(self.screen, self.blank_surface)

    def update(self):
        pass

    def draw(self):
        self.top_screen_camera.draw(self.top_screen_group)
        self.bottom_screen_camera.draw(self.bottom_screen_group)

        dirty = self.top_screen_group.draw(self.screen)
        dirty.extend(self.bottom_screen_group.draw(self.screen))

        return dirty

    def load(self):
        pass

    def unload(self):
        pass
