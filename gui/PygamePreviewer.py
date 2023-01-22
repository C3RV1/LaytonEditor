import threading

import k4pg
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
from typing import Any
import pygame as pg
import gc


# TODO: Move resource loading to pygame thread, as to not lag pyside thread


class PreviewerDefaultRenderer(TwoScreenRenderer):
    def __init__(self):
        super(PreviewerDefaultRenderer, self).__init__()
        sprite_loader = k4pg.SpriteLoaderOS(base_path_os="data_permanent/sprites")
        font_loader = k4pg.FontLoaderOS(base_path_os="data_permanent/fonts", fall_back_font_os="../font_default.json")
        self.tth_logo = k4pg.Sprite()
        sprite_loader.load("layton_editor_logo.png", self.tth_logo)
        self.tth_logo.set_size([240, 180], conserve_ratio=True, ratio_type=self.tth_logo.SNAP_MIN)
        self.previewer_text = k4pg.Text(text="Game Previewer", color=pg.Color(240, 240, 240))
        font_loader.load("consolas", 24, self.previewer_text)

    def unload(self):
        self.tth_logo.unload()
        self.previewer_text.unload()

    def draw(self):
        self.top_camera.clear(pg.Color(40, 40, 40))
        self.btm_camera.clear(pg.Color(40, 40, 40))
        self.tth_logo.draw(self.top_camera)
        self.previewer_text.draw(self.btm_camera)


class PygamePreviewer(threading.Thread):
    INSTANCE = None

    def __init__(self):
        super(PygamePreviewer, self).__init__()
        self.gm = k4pg.GameManager(k4pg.GameManagerConfig(
            screen_size=(256*TwoScreenRenderer.SCALE, 192*2*TwoScreenRenderer.SCALE),
            full_screen=False, window_name="Layton Editor Previewer",
            screen_pos=(100, 100)
        ))
        self.current_renderer: Any = PreviewerDefaultRenderer()
        self.loop_lock = threading.Lock()
        PygamePreviewer.INSTANCE = self

    def run(self) -> None:
        while self.gm.running:
            self.gm.tick()
            self.loop_lock.acquire()
            if not self.gm.running:
                break
            self.current_renderer.update(self.gm.delta_time)
            self.current_renderer.draw()
            self.loop_lock.release()

    def start_renderer(self, renderer: TwoScreenRenderer):
        self.loop_lock.acquire()
        if self.current_renderer:
            self.current_renderer.unload()
            gc.collect()
        self.current_renderer = renderer
        self.gm.post_load_clear()
        self.loop_lock.release()

    def stop_renderer(self):
        self.loop_lock.acquire()
        if self.current_renderer:
            self.current_renderer.unload()
            gc.collect()
        self.current_renderer = PreviewerDefaultRenderer()
        self.gm.post_load_clear()
        self.loop_lock.release()
