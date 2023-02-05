from pg_utils.rom.rom_extract import ORIGINAL_FPS
import k4pg


class EventWaiter:
    def __init__(self):
        self.current_wait_time = 0
        self.wait_tap = False
        self.inp = k4pg.Input()

    def wait(self, wait_frames):
        self.current_wait_time = wait_frames / ORIGINAL_FPS

    def do_wait_tap(self):
        self.wait_tap = True

    def busy(self):
        return self.current_wait_time > 0 or self.wait_tap

    def update_(self, dt: float):
        if self.current_wait_time > 0:
            self.current_wait_time -= dt
            if self.wait_tap and self.current_wait_time <= 0:
                self.wait_tap = False
        if self.inp.get_mouse_down(1) and self.wait_tap:
            self.wait_tap = False
            self.current_wait_time = 0
