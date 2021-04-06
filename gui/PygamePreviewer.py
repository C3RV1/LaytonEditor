import threading
from PygameEngine.GameManager import GameManager
from PygameEngine.Renderer import Renderer
from PygameEngine.Sprite import Sprite
from PygameEngine.UI.Text import Text
from pygame_utils.TwoScreenRenderer import TwoScreenRenderer
from typing import Optional
import pygame as pg


class PreviewerDefaultRenderer(TwoScreenRenderer):
    def __init__(self):
        super(PreviewerDefaultRenderer, self).__init__()
        self.tth_logo = Sprite(())
        self.previewer_text = Text(())

    def load(self):
        self.bottom_screen_group.add([self.tth_logo])
        self.top_screen_group.add([self.previewer_text])
        super(PreviewerDefaultRenderer, self).load()
        self.tth_logo.load("data_permanent/sprites/team_top_hat_logo.png")
        self.tth_logo.scale([128, 128], conserve_aspect_ratio=True)
        self.previewer_text.set_font("data_permanent/fonts/fontq.png", [7, 10], is_font_map=True)
        self.previewer_text.text = "Game Previewer"
        self.previewer_text.color = (240, 240, 240)

    def unload(self):
        super(PreviewerDefaultRenderer, self).unload()
        self.tth_logo.unload()
        self.previewer_text.unload()


class PygamePreviewer(threading.Thread):
    INSTANCE = None

    def __init__(self):
        super(PygamePreviewer, self).__init__()
        self.gm = GameManager(screen_size=[256*TwoScreenRenderer.SCALE, 192*2*TwoScreenRenderer.SCALE],
                              full_screen=False, name="Layton Editor Previewer",
                              screen_pos=[100, 100])
        self.current_renderer: Optional[Renderer] = None
        self.default_renderer = PreviewerDefaultRenderer()
        self.default_renderer.load()
        self.loop_lock = threading.Lock()
        PygamePreviewer.INSTANCE = self

    def run(self) -> None:
        while self.gm.running:
            self.gm.tick()
            self.loop_lock.acquire()
            if not self.gm.running:
                break
            if self.current_renderer:
                pg.display.update(self.current_renderer.run())
            else:
                pg.display.update(self.default_renderer.run())
            self.loop_lock.release()

    def start_renderer(self, renderer):
        self.loop_lock.acquire()
        if self.current_renderer:
            if self.current_renderer.loaded:
                self.current_renderer.unload()
        if self.default_renderer.loaded:
            self.default_renderer.unload()
        self.current_renderer: Renderer = renderer
        self.current_renderer.load()
        self.loop_lock.release()

    def stop_renderer(self):
        self.loop_lock.acquire()
        if self.current_renderer:
            if self.current_renderer.loaded:
                self.current_renderer.unload()
        self.current_renderer = None
        if not self.default_renderer.loaded:
            self.default_renderer.load()
        self.loop_lock.release()
