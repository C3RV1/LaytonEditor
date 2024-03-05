import k4pg
import pygame as pg


class ScreenFader(k4pg.Sprite):
    FADE_OUT = 1
    FADE_IN = 2
    DEFAULT_FADE_TIME = .7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha = 0
        self.fade = self.FADE_OUT
        self.fading = False
        self.current_time = 0
        self.fade_time = self.DEFAULT_FADE_TIME

        self.max_fade = 255

    def load_fader(self):
        surf = pg.Surface([256, 192])
        surf.fill(pg.Color(0, 0, 0))
        self.surf = surf

    def update(self, dt: float):
        if self.fading:
            self.current_time -= dt
            self.update_fade()

    def fade_in(self, instant_time=False):
        if instant_time:
            self.current_time = 0
        else:
            self.current_time = self.fade_time
        self.fade = self.FADE_IN
        self.fading = True

    def fade_out(self, instant_time=False):
        # if self.fade == self.FADING_OUT or instant_time:
        if instant_time:
            self.current_time = 0
        else:
            self.current_time = self.fade_time
        self.fade = self.FADE_OUT
        self.fading = True

    def set_fade(self, fade, instant_time=False):
        if instant_time:
            self.current_time = 0
        else:
            self.current_time = self.fade_time
        self.fade = fade
        self.fading = True

    def update_fade(self):
        percentage = 1 - min(max(self.current_time / self.fade_time, 0), 1)  # Clamp between 0 and 1
        if self.fade == self.FADE_OUT:
            self.alpha = self.max_fade * percentage
            if self.current_time <= 0:
                self.alpha = self.max_fade
                self.fading = False
        elif self.fade == self.FADE_IN:
            self.alpha = self.max_fade - self.max_fade * percentage
            if self.current_time <= 0:
                self.alpha = 0
                self.fading = False
        else:
            self.fading = False
