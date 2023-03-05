import k4pg
import pygame as pg
from pg_utils.ScreenFader import ScreenFader


class EventCharacter(k4pg.Sprite):
    FACING_LEFT = 1
    FACING_RIGHT = 2

    SLOT_MAX = 6
    SLOT_OFFSET = {0: 0, 1: 52*2 - 30,
                   2: 0, 3: 0,
                   4: 52, 5: 52,
                   6: 0}
    SLOT_ON_LEFT = [0, 3, 4]  # Verified against game binary
    SLOT_ON_RIGHT = [1, 2, 5, 6]

    FADE_TIME = 0.2

    slot: int
    char_id: int
    fading: bool
    fade_in: int
    current_fade_time: [int, float]
    talking: bool

    def __init__(self, *args, **kwargs):
        super(EventCharacter, self).__init__(*args, **kwargs)
        self.orientation = EventCharacter.FACING_RIGHT
        self.center.y = k4pg.Alignment.BOTTOM
        self.position.y = 192 // 2
        self.character_mouth: k4pg.Sprite = k4pg.Sprite()

    def setup(self, char_id, slot, anim_num, visibility):
        self.char_id = char_id
        self.slot = slot
        self.talking = False

        self.fading = False
        self.fade_in = ScreenFader.FADING_IN
        self.current_fade_time = 0

        if char_id == 0:
            return
        self.load_character()
        self.set_tag_by_num(anim_num)
        self.update_visibility(visibility)

    def set_tag(self, name: str):
        print(name)
        super(EventCharacter, self).set_tag(name)
        self.update_()

    def check_orientation(self):
        if self.slot in EventCharacter.SLOT_ON_LEFT:
            self.orientation = EventCharacter.FACING_RIGHT
        else:
            self.orientation = EventCharacter.FACING_LEFT

    def update_(self):
        if self.char_id == 0:
            return
        self.check_orientation()
        if self.orientation == EventCharacter.FACING_RIGHT:
            self.flipped = [True, False]
        else:
            self.flipped = [False, False]

        if self.orientation == EventCharacter.FACING_RIGHT:
            offset = EventCharacter.SLOT_OFFSET[self.slot] - 256 // 2
            self.center.x = k4pg.Alignment.LEFT
        else:
            offset = (256 // 2) - EventCharacter.SLOT_OFFSET[self.slot]
            self.center.x = k4pg.Alignment.RIGHT
        self.position.x = offset
        self.update_child()

    def update_child(self):
        mouth_offset = [self._active_tag.child_x, self._active_tag.child_y]
        world_rect = self.get_world_rect()
        if self.character_mouth is not None:
            if self.orientation == EventCharacter.FACING_RIGHT:
                mouth_offset[0] = world_rect.w - mouth_offset[0]
                self.character_mouth.center.x = k4pg.Alignment.RIGHT
                self.character_mouth.flipped = [True, False]
            else:
                self.character_mouth.center.x = k4pg.Alignment.LEFT
                self.character_mouth.flipped = [False, False]

            self.character_mouth.position.update(world_rect.x + mouth_offset[0],
                                                 self.position.y - world_rect.h + mouth_offset[1])
            self.character_mouth.center[1] = k4pg.Alignment.TOP
            self.character_mouth.set_tag_by_num(self._active_tag.child_index)
            if self._active_tag.child_index == 0:
                self.character_mouth.visible = False
            elif self.visible and not self.character_mouth.visible:
                self.character_mouth.visible = True

    def update_visibility(self, visible):
        if visible != self.visible:
            self.visible = visible
            if self.character_mouth is not None:
                self.character_mouth.visible = visible

    def show(self):
        self.update_visibility(True)

    def hide(self):
        self.update_visibility(False)

    def set_visibility(self, visibility, instant):
        self.fade_in = ScreenFader.FADING_IN if visibility else ScreenFader.FADING_OUT
        self.current_fade_time = self.FADE_TIME
        self.calc_fade()
        self.update_visibility(True)

    def calc_fade(self):
        alpha = int(255 * max(self.current_fade_time / self.FADE_TIME, 0.0))
        if self.fade_in == ScreenFader.FADING_IN:
            alpha = 255 - alpha
        self.alpha = alpha
        if self.character_mouth is not None:
            self.character_mouth.alpha = alpha

    def update_fade(self, dt: float):
        if self.current_fade_time > 0:
            self.current_fade_time -= dt
            self.calc_fade()

    def busy(self):
        return self.current_fade_time > 0.0

    def set_slot(self, slot):
        self.slot = slot
        self.update_()

    def set_anim(self, anim: str):
        anim = anim.replace("surprise", "suprise")
        self.set_tag(anim)
        if self.talking:
            self.set_talking()
        else:
            self.set_not_talking()

    def load_character(self):
        if self.char_id == 0:
            return
        self.loader.load(f"data_lt2/ani/eventchr/chr{self.char_id}.arc", self, True)
        if (drawoff := self.vars.get("drawoff", None)) is not None:
            self.position += pg.Vector2(drawoff[:2])
        if self.vars.get('child_image', "") != "":
            self.loader.load(f"data_lt2/ani/sub/chr{self.char_id}_face.arc", self.character_mouth, True)
        self.set_tag_by_num(1)

    def animate(self, dt: float):
        super(EventCharacter, self).animate(dt)
        if self.character_mouth:
            self.character_mouth.animate(dt)

    def set_talking(self):
        self.talking = True
        current_tag = self.get_tag().name
        if not current_tag.startswith("*") and self.get_tag_num() + 1 < self.tag_count:
            new_tag = self.tag_names[self.get_tag_num() + 1]
            if new_tag.startswith("*"):
                self.set_tag(new_tag)

    def set_not_talking(self):
        self.talking = False
        current_tag = self._active_tag.name
        if current_tag.endswith(" "):
            current_tag = current_tag[:-1]
        if current_tag.startswith("*"):
            self.set_tag(current_tag[1:])

    def __str__(self):
        return f"<Character {self.char_id}>"

    def __repr__(self):
        return f"<Character {self.char_id}>"

    def draw(self, cam: k4pg.Camera):
        super(EventCharacter, self).draw(cam)
        self.character_mouth.draw(cam)
