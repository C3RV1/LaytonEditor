import pg_engine as pge


class ScreenShaker(pge.Sprite):
    def __init__(self, *args, **kwargs):
        super(ScreenShaker, self).__init__(*args, **kwargs)
        self.shaking = False
        self.shake_intensity = 5
        self.shake_rotation = 0
        self.shake_rotation_speed = .5
        self.shake_time = 1.5
        self.current_shake_time = 0
        self.cycle = .05

    def update(self, dt: float):
        if self.shaking:
            self.current_shake_time -= dt
            self.update_shake()

    def update_shake(self):
        percentage = min(max(self.current_shake_time / self.shake_time, 0), 1)

        current_shake_intensity = self.shake_intensity * percentage

        cycle1 = (((self.current_shake_time // self.cycle) % 4) <= 1) * 2.0 - 1
        cycle2 = (((self.current_shake_time // self.cycle) % 4) % 2) * 2 - 1
        self.position = cycle1 * current_shake_intensity
        self.position = cycle2 * current_shake_intensity
        if percentage == 0:
            self.shaking = False

    def shake(self):
        self.shaking = True
        self.current_shake_time = self.shake_time
