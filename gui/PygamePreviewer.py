import threading
import pg_engine as pge
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
from typing import Any
import pygame as pg


class PreviewerDefaultRenderer(TwoScreenRenderer):
    def __init__(self):
        super(PreviewerDefaultRenderer, self).__init__()
        sprite_loader = pge.SpriteLoaderOS(base_path="data_permanent/sprites")
        font_loader = pge.FontLoaderOS(base_path="data_permanent/fonts")
        self.tth_logo = pge.Sprite()
        sprite_loader.load("team_top_hat_logo.png", self.tth_logo)
        self.tth_logo.set_size([128, 128], conserve_ratio=True, ratio_type=self.tth_logo.SNAP_MIN)
        self.previewer_text = pge.Text(text="Game Previewer", color=pg.Color(240, 240, 240))
        font_loader.load("consolas", 24, self.previewer_text)

    def unload(self):
        self.tth_logo.unload()
        self.previewer_text.unload()

    def draw(self):
        self.top_camera.surf.fill(pg.Color(40, 40, 40))
        self.tth_logo.draw(self.btm_camera)
        self.previewer_text.draw(self.top_camera)


class PygamePreviewer(threading.Thread):
    INSTANCE = None

    def __init__(self):
        super(PygamePreviewer, self).__init__()
        self.gm = pge.GameManager(pge.GameManagerConfig(
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
        self.current_renderer = renderer
        self.loop_lock.release()

    def stop_renderer(self):
        self.loop_lock.acquire()
        if self.current_renderer:
            self.current_renderer.unload()
        self.current_renderer = PreviewerDefaultRenderer()
        self.loop_lock.release()
