from .abstracts.EventBGAbstract import EventBGAbstract
from pygame_utils.ScreenShaker import ScreenShaker
from pygame_utils.ScreenFader import ScreenFader
from pygame_utils.rom.rom_extract import load_bg, ORIGINAL_FPS
import PygameEngine.Sprite
import pygame as pg


class EventBG(EventBGAbstract):
    def __init__(self, groups, name="unnamed"):
        super().__init__()
        self.bg = ScreenShaker(())
        self.bg.layer = -1000
        self.fader = ScreenFader(())
        self.fader.layer = 1000
        self.translucent = PygameEngine.Sprite.Sprite(())
        self.translucent.layer = -100

        self.bg.add(groups)
        self.fader.add(groups)
        self.translucent.add(groups)

        self.name = name

    def fade(self, fade_type, fade_time, instant):
        self.fader.set_fade(fade_type, False, instant_time=instant)
        if fade_time is not None:
            self.fader.current_time = fade_time / ORIGINAL_FPS
            self.fader.fade_time = fade_time / ORIGINAL_FPS
        else:
            self.fader.current_time = self.fader.DEFAULT_FADE_TIME
            self.fader.fade_time = self.fader.DEFAULT_FADE_TIME
        if instant:
            self.fader.current_time = 0
            self.fader.fade_time = self.fader.DEFAULT_FADE_TIME
        self.fader.update_fade()

    def shake(self):
        self.bg.shake()

    def set_bg(self, path):
        load_bg(path, self.bg)
        self.set_opacity(0)

    @property
    def shaking(self):
        return self.bg.shaking

    @property
    def fading(self):
        return self.fader.fading

    def set_opacity(self, opacity):
        self.translucent.set_alpha(opacity)

    def set_fade_max_opacity(self, opacity):
        self.fader.max_fade = opacity

    def add(self, groups):
        self.bg.add(groups)
        self.fader.add(groups)
        self.translucent.add(groups)

    def kill(self):
        self.bg.kill()
        self.fader.kill()
        self.translucent.kill()

    def load(self):
        self.fader.load_fader()
        self.translucent.original_image = pg.Surface([256, 192])
        self.translucent.original_image.fill(pg.Color(0, 0, 0))

    def unload(self):
        self.bg.unload()
        self.fader.unload()
        self.translucent.unload()

    def update_(self):
        self.fader.update_()
        self.bg.update_()

    def busy(self):
        return self.fading

    def __str__(self):
        return f"<EventBG {self.name}>"
