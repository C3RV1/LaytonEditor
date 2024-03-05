import copy

from pg_utils.ScreenShaker import ScreenShaker
from pg_utils.ScreenFader import ScreenFader
import k4pg
import pygame as pg
from previewers.event.state.EventBGState import EventBGState
from k4pg.sprite.SpriteLoader import SpriteLoader


class EventBG:
    def __init__(self, loader: SpriteLoader, name="unnamed"):
        self.bg = ScreenShaker()
        self.fader = ScreenFader()
        self.fader.load_fader()
        self.translucent = k4pg.Sprite()
        surf = pg.Surface([256, 192])
        self.translucent.surf = surf

        self.loader = loader
        self.state = EventBGState("", self.fader.fade, (0, 0, 0))
        self.name = name

    def load_background(self, background: str, instant: bool):
        self.state.background = background
        if not instant:
            self.loader.load(background, self.bg, sprite_sheet=False)

    def fade(self, fade_type: int, fade_time, instant: bool, editing: bool):
        if fade_type == self.fader.fade:
            return

        if editing:
            self.fader.max_fade = 100
        else:
            self.fader.max_fade = 255

        if fade_time == 0:
            instant = True

        if fade_time is not None:
            self.fader.current_time = fade_time / 60.0
            self.fader.fade_time = fade_time / 60.0
        else:
            self.fader.current_time = self.fader.DEFAULT_FADE_TIME
            self.fader.fade_time = self.fader.DEFAULT_FADE_TIME

        self.state.fade = fade_type
        self.fader.set_fade(fade_type, instant_time=instant)
        self.fader.update_fade()

    def shake(self):
        self.bg.shake()

    @property
    def shaking(self):
        return self.bg.shaking

    @property
    def fading(self):
        return self.fader.fading

    def set_tint(self, colors: tuple, instant: bool):
        self.state.tint = colors
        if not instant:
            self.translucent.surf.fill(pg.Color(colors[:3]))
            self.translucent.surf_updated()
            self.translucent.alpha = colors[-1]

    def update_(self, dt: float):
        self.fader.update(dt)
        self.bg.update(dt)

    def draw_back(self, cam: k4pg.Camera):
        self.bg.draw(cam)
        self.translucent.draw(cam)

    def draw_front(self, cam: k4pg.Camera):
        self.fader.draw(cam)

    def busy(self) -> bool:
        return self.fading

    def copy_state(self) -> EventBGState:
        return copy.copy(self.state)

    def load_state(self, state: EventBGState, editing: bool):
        self.load_background(state.background, False)
        self.set_tint(state.tint, False)
        self.fade(state.fade, None, True, editing)

    def sync_state(self, editing: bool):
        self.load_background(self.state.background, False)
        self.set_tint(self.state.tint, False)
        self.fade(self.state.fade, None, True, editing)

    def __str__(self):
        return f"<EventBG {self.name}>"
