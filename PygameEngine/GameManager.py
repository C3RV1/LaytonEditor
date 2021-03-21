import pygame
import random
import time
from .Debug import Debug
from .Screen import Screen
from .Input import Input


class GameManager(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(GameManager.__instance, GameManager):
            GameManager.__instance = super(GameManager, cls).__new__(cls)
        return GameManager.__instance

    def __del__(self):
        self.exit()

    def __init__(self, screen_size=None, full_screen=True, log_fps=False, fps_limit=60, name="Default Name"):
        if not GameManager.__inited or not self.running:
            pygame.init()
            pygame.mixer.init()

            self.running = True

            if not screen_size:
                Debug.log_error("Screen size not specified", "GameManager")
                self.exit()
                return

            GameManager.__inited = True
            flags = pygame.HWSURFACE | pygame.DOUBLEBUF
            if full_screen:
                flags = flags | pygame.FULLSCREEN
            Screen.new_screen(screen_size, flags, name=name)

            self._delta_time = 1
            self.time_scale = 1

            self.pygame_clock = pygame.time.Clock()  # type: pygame
            self.pygame_clock.tick()

            self.log_fps = log_fps

            self.input_manager = Input()

            random.seed(time.time())

            self.fps_cap = fps_limit
            self.events = []

    def tick(self):
        self._delta_time = self.pygame_clock.tick(self.fps_cap) / 1000.0
        self.events = pygame.event.get()
        self.input_manager.update_events(self.events)

        if self.log_fps:
            Debug.log(f"FPS: { 1 / self._delta_time }", self)

    @property
    def delta_time(self):
        return self._delta_time * self.time_scale

    def exit(self):
        if self.running:
            self.running = False
            pygame.quit()
