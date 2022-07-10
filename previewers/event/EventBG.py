from pg_utils.ScreenShaker import ScreenShaker
from pg_utils.ScreenFader import ScreenFader
import k4pg
import pygame as pg


class EventBG:
    def __init__(self, name="unnamed"):
        self.bg = ScreenShaker()
        self.fader = ScreenFader()
        self.fader.load_fader()
        self.translucent = k4pg.Sprite()
        surf = pg.Surface([256, 192])
        surf.fill(pg.Color(0, 0, 0))
        self.translucent.surf = surf
        self.translucent.alpha = 0

        self.name = name

    def fade(self, fade_type, fade_time, instant):
        if fade_type == self.fader.fade:
            return
        self.fader.set_fade(fade_type, False, instant_time=instant)
        if fade_time is not None:
            self.fader.current_time = fade_time / 60.0
            self.fader.fade_time = fade_time / 60.0
        else:
            self.fader.current_time = self.fader.DEFAULT_FADE_TIME
            self.fader.fade_time = self.fader.DEFAULT_FADE_TIME
        if instant:
            self.fader.current_time = 0
            self.fader.fade_time = self.fader.DEFAULT_FADE_TIME
        self.fader.update_fade()

    def shake(self):
        self.bg.shake()

    @property
    def shaking(self):
        return self.bg.shaking

    @property
    def fading(self):
        return self.fader.fading

    def set_opacity(self, opacity):
        self.translucent.alpha = opacity

    def unload(self):
        self.bg.unload()
        self.fader.unload()
        self.translucent.unload()

    def update_(self, dt: float):
        self.fader.update(dt)
        self.bg.update(dt)

    def draw_back(self, cam: k4pg.Camera):
        self.bg.draw(cam)
        self.translucent.draw(cam)

    def draw_front(self, cam: k4pg.Camera):
        self.fader.draw(cam)

    def busy(self):
        return self.fading

    def __str__(self):
        return f"<EventBG {self.name}>"
