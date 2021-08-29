import pg_engine as pge
import pygame as pg


class TwoScreenRenderer:
    SCALE = 2

    def __init__(self):
        self.gm = pge.GameManager()

        screen = pge.Screen.screen()
        self.top_camera = pge.Camera(screen, viewport=pg.rect.Rect(0, 0, 256 * TwoScreenRenderer.SCALE,
                                                                   192 * TwoScreenRenderer.SCALE),
                                     zoom=[TwoScreenRenderer.SCALE, TwoScreenRenderer.SCALE])

        self.btm_camera = pge.Camera(screen, viewport=pg.rect.Rect(0, 192 * TwoScreenRenderer.SCALE,
                                                                   256 * TwoScreenRenderer.SCALE,
                                                                   192 * TwoScreenRenderer.SCALE),
                                     zoom=[TwoScreenRenderer.SCALE, TwoScreenRenderer.SCALE])

        self.running = True

    def exit(self):
        self.gm.exit()

    def clear(self):
        self.top_camera.surf.fill((0, 0, 0), self.top_camera.viewport)
        self.btm_camera.surf.fill((0, 0, 0), self.btm_camera.viewport)

    def update(self, dt: float):
        pass

    def draw(self):
        pass

    def load(self):
        pass

    def unload(self):
        pass
