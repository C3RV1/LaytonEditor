import PygameEngine.GameManager
import pygame as pg
import PygameEngine.Sprite
import PygameEngine.Camera
import PygameEngine.Input
import PygameEngine.Screen
import PygameEngine.Animation
from PygameEngine import Renderer


class TwoScreenRenderer(Renderer.Renderer):
    SCALE = 2

    def __init__(self):
        super(TwoScreenRenderer, self).__init__()
        self.top_screen_group = pg.sprite.LayeredDirty()
        self.bottom_screen_group = pg.sprite.LayeredDirty()

        self.top_screen_camera = PygameEngine.Camera.Camera()
        self.top_screen_camera.display_port = pg.rect.Rect(0, 0, 256 * TwoScreenRenderer.SCALE,
                                                           192 * TwoScreenRenderer.SCALE)
        self.top_screen_camera.scale = TwoScreenRenderer.SCALE

        self.bottom_screen_camera = PygameEngine.Camera.Camera()
        self.bottom_screen_camera.display_port = pg.rect.Rect(0, 192 * TwoScreenRenderer.SCALE,
                                                              256 * TwoScreenRenderer.SCALE,
                                                              192 * TwoScreenRenderer.SCALE)
        self.bottom_screen_camera.scale = TwoScreenRenderer.SCALE

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
        if not self.just_loaded:
            self.top_screen_camera.draw(self.top_screen_group)
            dirty = self.top_screen_group.draw(self.screen)
            self.bottom_screen_camera.draw(self.bottom_screen_group)
            dirty.extend(self.bottom_screen_group.draw(self.screen))
        else:
            self.top_screen_camera.draw(self.top_screen_group)
            self.top_screen_group.repaint_rect(self.top_screen_camera.display_port)
            self.bottom_screen_camera.draw(self.bottom_screen_group)
            self.bottom_screen_group.repaint_rect(self.bottom_screen_camera.display_port)
            self.just_loaded = False
            return [pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])]

        return dirty

    def load(self):
        super(TwoScreenRenderer, self).load()

    def unload(self):
        super(TwoScreenRenderer, self).unload()
