from .abstracts.EventWaiterAbstract import EventWaiterAbstract
from pygame_utils.rom.rom_extract import ORIGINAL_FPS
import PygameEngine.GameManager


class EventWaiter(EventWaiterAbstract):
    def __init__(self):
        super().__init__()
        self.gm = PygameEngine.GameManager.GameManager()
        self.current_wait_time = 0

    def wait(self, wait_frames):
        self.current_wait_time = wait_frames / ORIGINAL_FPS

    def busy(self):
        return self.current_wait_time > 0

    def stop(self):
        self.current_wait_time = 0

    def update_(self):
        if self.current_wait_time > 0:
            self.current_wait_time -= self.gm.delta_time
