import k4pg
import pygame as pg


class TwoScreenRenderer:
    SCALE = 2

    def __init__(self):
        self.gm = k4pg.GameManager()

        screen = k4pg.Screen.screen()
        self.top_camera = k4pg.Camera(screen, viewport=pg.rect.Rect(0, 0, 256 * TwoScreenRenderer.SCALE,
                                                                    192 * TwoScreenRenderer.SCALE),
                                      zoom=pg.Vector2(TwoScreenRenderer.SCALE, TwoScreenRenderer.SCALE))

        self.btm_camera = k4pg.Camera(screen, viewport=pg.rect.Rect(0, 192 * TwoScreenRenderer.SCALE,
                                                                    256 * TwoScreenRenderer.SCALE,
                                                                    192 * TwoScreenRenderer.SCALE),
                                      zoom=pg.Vector2(TwoScreenRenderer.SCALE, TwoScreenRenderer.SCALE))

        self.running = True

    def exit(self):
        self.gm.exit()

    def clear(self):
        self.top_camera.clear(pg.Color(0, 0, 0))
        self.btm_camera.clear(pg.Color(0, 0, 0))

    def update(self, dt: float):
        pass

    def draw(self):
        pass

    def load(self):
        pass

    def unload(self):
        pass
