from pg_engine import Sprite, Input, Camera, Alignment


class Slider(Sprite):
    def __init__(self, *args, min_value=0, max_value=100, start_value=0, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)
        self.child = Sprite()
        self.inp = Input()
        self.range = [min_value, max_value - min_value]
        self.percentage = (start_value - min_value) / self.range[1]
        self.interacting = False

    def update_child_pos(self):
        world_rect = self.get_world_rect()
        self.child.position[0] = (self.percentage * world_rect.w) + world_rect.x
        self.child.position[1] = world_rect.y + world_rect.h / 2
        self.child.center = [Alignment.CENTER, Alignment.CENTER]
        self.child.visible = self.visible

    def get_value(self, cam: Camera):
        screen_rect = self.get_screen_rect(cam, do_clip=False)[0]
        changed = False
        if screen_rect.w == 0:
            return
        if self.inp.get_mouse_down(1) and not self.interacting:
            screen_pos = self.inp.get_mouse_pos()
            if screen_rect.collidepoint(screen_pos[0], screen_pos[1]):
                self.interacting = True
                self.inp.grab_mouse(id(self))
        if self.interacting:
            if self.inp.get_mouse_up(1, id(self)):
                self.interacting = False
                self.inp.release_mouse()
            else:
                screen_pos = self.inp.get_mouse_pos(id(self))
                self.percentage = (screen_pos[0] - screen_rect.x) / screen_rect.w
                self.percentage = max(self.percentage, 0)
                self.percentage = min(self.percentage, 1)
                changed = True
        return self.percentage * self.range[1] + self.range[0], changed

    def draw(self, cam: Camera):
        self.update_child_pos()
        super().draw(cam)
        self.child.draw(cam)
