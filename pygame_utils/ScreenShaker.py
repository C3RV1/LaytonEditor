import PygameEngine.Sprite
import PygameEngine.GameManager

from PygameEngine.Debug import Debug


class ScreenShaker(PygameEngine.Sprite.Sprite):
    def __init__(self, groups):
        super(ScreenShaker, self).__init__(groups)
        self.gm = PygameEngine.GameManager.GameManager()

        self.shaking = False
        self.shake_intensity = 5
        self.shake_rotation = 0
        self.shake_rotation_speed = .5
        self.shake_time = 1.5
        self.current_shake_time = 0
        self.cycle = .05

    def update_(self):
        if self.shaking:
            self.current_shake_time -= self.gm.delta_time
            self.update_shake()

    def update_shake(self):
        percentage = min(max(self.current_shake_time / self.shake_time, 0), 1)

        current_shake_intensity = self.shake_intensity * percentage

        cycle1 = (((self.current_shake_time // self.cycle) % 4) <= 1) * 2.0 - 1
        cycle2 = (((self.current_shake_time // self.cycle) % 4) % 2) * 2 - 1
        self.world_rect.x = cycle1 * current_shake_intensity
        self.world_rect.y = cycle2 * current_shake_intensity
        if percentage == 0:
            self.shaking = False

    def shake(self):
        self.shaking = True
        self.current_shake_time = self.shake_time
