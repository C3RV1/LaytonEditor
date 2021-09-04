from pg_utils.rom.rom_extract import ORIGINAL_FPS


class EventWaiter:
    def __init__(self):
        self.current_wait_time = 0

    def wait(self, wait_frames):
        self.current_wait_time = wait_frames / ORIGINAL_FPS

    def busy(self):
        return self.current_wait_time > 0

    def stop(self):
        self.current_wait_time = 0

    def update_(self, dt: float):
        if self.current_wait_time > 0:
            self.current_wait_time -= dt
