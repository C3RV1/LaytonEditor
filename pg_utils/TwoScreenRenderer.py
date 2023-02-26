import k4pg
import pygame as pg


class TwoScreenRenderer:
    SCALE = 2

    def __init__(self):
        self.gm = k4pg.GameManager()
        self.inp = k4pg.Input()

        screen = k4pg.Screen.screen()
        self.top_camera = k4pg.Camera(screen, viewport=pg.rect.Rect(0, 0, 256 * TwoScreenRenderer.SCALE,
                                                                    192 * TwoScreenRenderer.SCALE),
                                      zoom=pg.Vector2(TwoScreenRenderer.SCALE, TwoScreenRenderer.SCALE))

        self.btm_camera = k4pg.Camera(screen, viewport=pg.rect.Rect(0, 192 * TwoScreenRenderer.SCALE,
                                                                    256 * TwoScreenRenderer.SCALE,
                                                                    192 * TwoScreenRenderer.SCALE),
                                      zoom=pg.Vector2(TwoScreenRenderer.SCALE, TwoScreenRenderer.SCALE))

        self.cursor_font_loader = k4pg.FontLoaderSYS()

        self.show_cursor_pos = False
        self.cursor_pos = k4pg.Text(position=pg.Vector2(-256//2, 192//2),
                                    center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.BOTTOM),
                                    scale=pg.Vector2(1/TwoScreenRenderer.SCALE, 1/TwoScreenRenderer.SCALE))
        self.cursor_font_loader.load("arial", 24, self.cursor_pos)
        self.running = True

    def exit(self):
        self.gm.exit()

    def clear(self):
        self.top_camera.clear(pg.Color(0, 0, 0))
        self.btm_camera.clear(pg.Color(0, 0, 0))

    def update(self, dt: float):
        cursor_pos = pg.Vector2(self.inp.get_mouse_pos()) / TwoScreenRenderer.SCALE
        x = int(cursor_pos.x)
        y = int(cursor_pos.y) % 192
        screen = int(cursor_pos.y / 192)
        screen = {
            0: "Top",
            1: "Bottom"
        }[screen]
        self.cursor_pos.text = f"Cursor: {x}, {y} ({screen})"

    def draw(self):
        if self.show_cursor_pos:
            self.cursor_pos.draw(self.btm_camera)

    def load(self):
        pass

    def unload(self):
        pass
