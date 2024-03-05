import copy

import k4pg
import pygame as pg
from pg_utils.ScreenFader import ScreenFader
from previewers.event.state.EventCharacterState import EventCharacterState


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

    def __init__(self, character_id, slot, anim_num, visibility, loader, *args, **kwargs):
        super(EventCharacter, self).__init__(*args, **kwargs)
        self.state = EventCharacterState(slot, ScreenFader.FADE_OUT, visibility, False)

        self.orientation = EventCharacter.FACING_RIGHT
        self.center.y = k4pg.Alignment.BOTTOM
        self.position.y = 192 // 2
        self.slot = slot
        self.character_mouth: k4pg.Sprite = k4pg.Sprite()

        self.char_id = character_id

        self.talking = False

        self.load_character(loader)
        self.set_tag_by_num(anim_num)
        self.state.anim = self.get_tag().name
        self.update_visibility(visibility)

        self.fading = False
        self.fade = ScreenFader.FADE_IN
        self.state.fade = True
        self.current_fade_time = 0

    def set_tag(self, name: str):
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
            self.state.visible = visible
            self.visible = visible
            if self.character_mouth is not None:
                self.character_mouth.visible = visible

    def show(self):
        self.update_visibility(True)

    def hide(self):
        self.update_visibility(False)

    def set_opacity(self, visibility, instant=False):
        self.fade = ScreenFader.FADE_IN if visibility else ScreenFader.FADE_OUT
        self.state.fade = visibility
        if not instant:
            self.current_fade_time = self.FADE_TIME
        else:
            self.current_fade_time = 0
        self.update_fade(0)
        self.update_visibility(True)

    def update_fade(self, dt: float):
        if self.current_fade_time >= 0:
            self.current_fade_time -= dt
            alpha = int(255 * max(self.current_fade_time / self.FADE_TIME, 0.0))
            if self.fade == ScreenFader.FADE_IN:
                alpha = 255 - alpha
            self.alpha = alpha
            if self.character_mouth is not None:
                self.character_mouth.alpha = alpha

    def busy(self):
        return self.current_fade_time > 0.0

    def set_slot(self, slot):
        self.slot = slot
        self.state.slot = slot
        self.update_()

    def set_anim(self, anim: str):
        self.state.anim = anim
        anim = anim.replace("surprise", "suprise")
        self.set_tag(anim)
        if self.talking:
            self.set_talking(True)
        else:
            self.set_talking(False)

    def load_character(self, loader: k4pg.SpriteLoader):
        if loader:
            loader.load(f"data_lt2/ani/eventchr/chr{self.char_id}.arc", self, True)
        if (drawoff := self.vars.get("drawoff", None)) is not None:
            self.position += pg.Vector2(drawoff[:2])
        if self.vars.get('child_image', "") != "" and loader:
            loader.load(f"data_lt2/ani/sub/{self.vars['child_image']}", self.character_mouth, True)
        self.set_tag_by_num(1)

    def animate(self, dt: float):
        super(EventCharacter, self).animate(dt)
        if self.character_mouth:
            self.character_mouth.animate(dt)

    def set_talking(self, talking: bool):
        if self.talking == talking:
            return
        self.talking = talking
        current_tag = self.get_tag().name
        if self.talking:
            if not current_tag.startswith("*") and self.get_tag_num() + 1 < self.tag_count:
                new_tag = self.tag_names[self.get_tag_num() + 1]
                if new_tag.startswith("*"):
                    self.set_tag(new_tag)
        else:
            if current_tag.endswith(" "):
                current_tag = current_tag[:-1]
            if current_tag.startswith("*"):
                self.set_tag(current_tag[1:])

    def get_char_id(self):
        return self.char_id

    def __str__(self):
        return f"<Character {self.char_id}>"

    def __repr__(self):
        return f"<Character {self.char_id}>"

    def draw(self, cam: k4pg.Camera):
        super(EventCharacter, self).draw(cam)
        self.character_mouth.draw(cam)

    def copy_state(self) -> EventCharacterState:
        return copy.copy(self.state)

    def load_state(self, state: EventCharacterState):
        self.set_anim(state.anim)
        self.set_opacity(state.fade, True)
        self.update_visibility(state.visible)
        self.set_slot(state.slot)
        self.set_talking(self.talking)
