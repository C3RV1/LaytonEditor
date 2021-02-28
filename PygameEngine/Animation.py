import PygameEngine.Sprite
import PygameEngine.GameManager


class Animation(PygameEngine.Sprite.Sprite):
    def __init__(self, groups):
        PygameEngine.Sprite.Sprite.__init__(self, groups)
        self._current_time = 0
        self.gm = PygameEngine.GameManager.GameManager()

        self.current_tag = None

        self.anim_frame = 0
        self.default_duration = 200
        self.duration = self.default_duration

    def update_animation(self, delta_time=None):
        if delta_time is None:
            delta_time = self.gm.delta_time
        self._current_time += delta_time
        self.update_anim_duration()
        while self._current_time >= self.duration:
            self._current_time -= self.duration
            self.anim_frame += 1
            self.update_anim_duration()
        self.update_anim_frame()

    def update_anim_frame(self):
        if self.current_tag is None:
            return
        if len(self.current_tag["frames"]) == 0:
            return
        self.anim_frame %= len(self.current_tag["frames"])
        pre_frame = self.frame
        self.frame = self.current_tag["frames"][self.anim_frame]

        if pre_frame != self.frame:
            self._update_frame_info()

        self.update_anim_duration()

    def update_anim_duration(self):
        if "duration" in self.sprite_sheet_info["frames"][self.frame].keys():
            self.duration = self.sprite_sheet_info["frames"][self.frame]["duration"]
            if self.duration is not None:
                self.duration /= 1000
            else:
                self.duration = self.default_duration

    def set_tag(self, tag_name):
        for tag in self.sprite_sheet_info["meta"]["frameTags"]:
            if tag["name"] == tag_name:
                self.current_tag = tag
                break
        self.anim_frame = 0
        self.update_anim_frame()
        self.update_frame()

    def set_tag_by_num(self, tag_num):
        tag_name = self.sprite_sheet_info["meta"]["frameTags"][tag_num]["name"]
        self.set_tag(tag_name)
