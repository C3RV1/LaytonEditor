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
        self.top_group = pg.sprite.LayeredDirty()
        self.btm_group = pg.sprite.LayeredDirty()

        self.top_camera = PygameEngine.Camera.Camera()
        self.top_camera.display_port = pg.rect.Rect(0, 0, 256 * TwoScreenRenderer.SCALE,
                                                    192 * TwoScreenRenderer.SCALE)
        self.top_camera.scale = TwoScreenRenderer.SCALE

        self.btm_camera = PygameEngine.Camera.Camera()
        self.btm_camera.display_port = pg.rect.Rect(0, 192 * TwoScreenRenderer.SCALE,
                                                    256 * TwoScreenRenderer.SCALE,
                                                    192 * TwoScreenRenderer.SCALE)
        self.btm_camera.scale = TwoScreenRenderer.SCALE

        self.top_group.set_clip(self.top_camera.display_port)
        self.btm_group.set_clip(self.btm_camera.display_port)

        self.running = True

    def exit(self):
        self.gm.exit()

    def clear(self):
        self.top_group.clear(self.screen, self.blank_surface)
        self.btm_group.clear(self.screen, self.blank_surface)

    def update(self):
        pass

    def draw(self):
        if not self.just_loaded:
            self.top_camera.draw(self.top_group)
            dirty = self.top_group.draw(self.screen)
            self.btm_camera.draw(self.btm_group)
            dirty.extend(self.btm_group.draw(self.screen))
        else:
            self.top_camera.draw(self.top_group)
            self.top_group.repaint_rect(self.top_camera.display_port)
            self.btm_camera.draw(self.btm_group)
            self.btm_group.repaint_rect(self.btm_camera.display_port)
            self.just_loaded = False
            return [pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])]

        return dirty

    def load(self):
        super(TwoScreenRenderer, self).load()

    def unload(self):
        super(TwoScreenRenderer, self).unload()
