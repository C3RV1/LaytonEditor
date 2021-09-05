import pg_engine as pge
import pygame as pg


class ScreenFader(pge.Sprite):
    FADING_OUT = 1
    FADING_IN = 2
    DEFAULT_FADE_TIME = .7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha = 0
        self.fade = self.FADING_OUT
        self.fading = False
        self.current_time = 0
        self.fade_time = self.DEFAULT_FADE_TIME
        self.on_finish_fade = lambda fade_type: None
        self.run_on_finish_fade = True

        self.max_fade = 255

    def load_fader(self):
        surf = pg.Surface([256, 192])
        surf.fill(pg.Color(0, 0, 0))
        self.surf = surf

    def update(self, dt: float):
        if self.fading:
            self.current_time -= dt
            self.update_fade()

    def finish_fade(self):
        if self.run_on_finish_fade:
            self.on_finish_fade(self.fade)

    def fade_in(self, run_fade_finish, instant_time=False):
        if instant_time:
            self.current_time = 0
        else:
            self.current_time = self.fade_time
        self.fade = self.FADING_IN
        self.fading = True
        self.run_on_finish_fade = run_fade_finish

    def fade_out(self, run_fade_finish, instant_time=False):
        # if self.fade == self.FADING_OUT or instant_time:
        if instant_time:
            self.current_time = 0
        else:
            self.current_time = self.fade_time
        self.fade = self.FADING_OUT
        self.fading = True
        self.run_on_finish_fade = run_fade_finish

    def set_fade(self, fade, run_fade_finish, instant_time=False):
        if instant_time:
            self.current_time = 0
        else:
            self.current_time = self.fade_time
        self.fade = fade
        self.fading = True
        self.run_on_finish_fade = run_fade_finish

    def update_fade(self):
        if self.current_time <= 0:
            percentage = 0
        else:
            percentage = 1 - min(max(self.current_time / self.fade_time, 0), 1)  # Clamp between 0 and 1
        if self.fade == self.FADING_OUT:
            self.alpha = self.max_fade * percentage
            if self.current_time <= 0:
                self.alpha = self.max_fade
                self.fading = False
                self.finish_fade()
        elif self.fade == self.FADING_IN:
            self.alpha = self.max_fade - self.max_fade * percentage
            if self.current_time <= 0:
                self.alpha = 0
                self.fading = False
                self.finish_fade()
        else:
            self.finish_fade()
            self.fading = False
