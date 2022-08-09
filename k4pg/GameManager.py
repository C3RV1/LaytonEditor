import pygame as pg
import random
import time
from .Screen import Screen
from .input.Input import Input
import os
from dataclasses import dataclass


@dataclass
class GameManagerConfig:
    screen_size: tuple
    full_screen: bool = True
    log_fps: bool = False
    fps_limit: int = 60
    window_name: str = "Default Name"
    screen_pos: tuple = None


class GameManager(object):
    __instance = None
    __inited = False
    version = "k4pg v1.1.2"

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(GameManager.__instance, GameManager):
            GameManager.__instance = super(GameManager, cls).__new__(cls)
        return GameManager.__instance

    def __del__(self):
        self.exit()

    def __init__(self, gm_config: GameManagerConfig = None):
        if not GameManager.__inited and gm_config:
            print(f"Starting {self.version} with config {gm_config}")
            # Set screen position
            if gm_config.screen_pos is not None:
                os.environ["SDL_VIDEO_WINDOW_POS"] = f"{gm_config.screen_pos[0]},{gm_config.screen_pos[1]}"

            # Initialize pygame
            pg.init()
            pg.mixer.init()

            self._running: bool = True
            self._delta_time: float = 1.0
            self.time_scale: float = 1.0
            self._pygame_clock: pg.time.Clock = pg.time.Clock()
            self.log_fps: bool = gm_config.log_fps
            self.fps_cap: int = gm_config.fps_limit
            self.input_manager: Input = Input()
            self._events: list = []

            # Create screen
            flags = pg.HWSURFACE | pg.DOUBLEBUF
            if gm_config.full_screen:
                flags = flags | pg.FULLSCREEN
            Screen.new_screen(gm_config.screen_size, flags, name=gm_config.window_name)

            # Randomize
            random.seed(time.time())

            # Tick time for first time
            self._pygame_clock.tick()

            GameManager.__inited = True

    def post_load_clear(self):
        self._delta_time = 0
        self.input_manager.update_events([])

    def tick(self):
        if not self._running:
            return
        pg.display.flip()
        self._delta_time = self._pygame_clock.tick(self.fps_cap) / 1000.0
        self._events = pg.event.get()
        self.input_manager.update_events(self._events)

        if self.log_fps:
            print(f"FPS: { 1 / self._delta_time }", self)

    @property
    def delta_time(self):
        return self._delta_time * self.time_scale

    def exit(self):
        if self._running:
            self._running = False
            pg.quit()

    @property
    def running(self):
        return self._running
