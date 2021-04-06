import PygameEngine.Animation
import PygameEngine.Sprite
import PygameEngine.UI.UIElement
import PygameEngine.Input
from .abstracts.EventCharacterAbstract import EventCharacterAbstract
from pygame_utils.rom.rom_extract import load_animation
import PygameEngine.Debug


class EventCharacter(PygameEngine.Animation.Animation, EventCharacterAbstract):
    FACING_LEFT = 1
    FACING_RIGHT = 2

    SLOT_MAX = 6
    SLOT_OFFSET = {0: 0, 1: 0,
                   2: 0, 3: 0,
                   4: 52, 5: 52,
                   6: 0}
    SLOT_ON_LEFT = [0, 3, 4]  # Verified against game binary
    SLOT_ON_RIGHT = [2, 5, 6]

    def __init__(self, groups):
        PygameEngine.Animation.Animation.__init__(self, groups)
        EventCharacterAbstract.__init__(self)
        self.orientation = EventCharacter.FACING_RIGHT
        self.draw_alignment[1] = PygameEngine.Sprite.Sprite.ALIGNMENT_TOP
        self.world_rect.y += 192 // 2
        self.slot = 0
        self.character_mouth = PygameEngine.Animation.Animation([])
        self.character_mouth.layer = 10
        self.character_mouth.add(groups)

        self.groups_perseverance = groups

        self.char_id = 0

    def check_orientation(self):
        if self.slot in EventCharacter.SLOT_ON_LEFT:
            self.orientation = EventCharacter.FACING_RIGHT
        else:
            self.orientation = EventCharacter.FACING_LEFT

    def update_(self):
        if self.char_id == 0:
            return
        self.update_anim_frame()
        self.check_orientation()
        if self.orientation == EventCharacter.FACING_RIGHT:
            self.flip(True, False)
        else:
            self.flip(False, False)

        if self.orientation == EventCharacter.FACING_RIGHT:
            offset = EventCharacter.SLOT_OFFSET[self.slot] - 256 // 2
            self.draw_alignment[0] = self.ALIGNMENT_RIGHT
        else:
            offset = (256 // 2) - EventCharacter.SLOT_OFFSET[self.slot]
            self.draw_alignment[0] = self.ALIGNMENT_LEFT
        self.world_rect.x = offset
        self.update_child()
        self.dirty = 1

    def update_child(self):
        mouth_offset = [self.current_tag["child_x"], self.current_tag["child_y"]]
        if self.character_mouth is not None:
            if self.orientation == EventCharacter.FACING_RIGHT:
                mouth_offset[0] = self.world_rect.w - mouth_offset[0]
                self.character_mouth.draw_alignment[0] = self.ALIGNMENT_LEFT
                self.character_mouth.flip(True, False)
            else:
                mouth_offset[0] = mouth_offset[0] - self.world_rect.w
                self.character_mouth.draw_alignment[0] = self.ALIGNMENT_RIGHT
                self.character_mouth.flip(False, False)

            self.character_mouth.world_rect.x = self.world_rect.x + mouth_offset[0]
            self.character_mouth.world_rect.y = self.world_rect.y - self.world_rect.h + mouth_offset[1]
            self.character_mouth.draw_alignment[1] = self.ALIGNMENT_BOTTOM
            self.character_mouth.set_tag_by_num(self.current_tag["child_index"])
            if self.current_tag["child_index"] == 0:
                self.character_mouth.kill()
            elif self.alive() and not self.character_mouth.alive():
                self.character_mouth.add(self.groups())
            self.character_mouth.dirty = 1
        self.dirty = 1

    def show(self):
        if not self.alive():
            self.add(self.groups_perseverance)
            if self.character_mouth is not None:
                self.character_mouth.add(self.groups_perseverance)
        self.dirty = 1
        if self.character_mouth is not None:
            self.character_mouth.dirty = 1

    def hide(self):
        if self.alive():
            self.kill()
            if self.character_mouth is not None:
                self.character_mouth.kill()
        self.dirty = 1
        if self.character_mouth is not None:
            self.character_mouth.dirty = 1

    def set_visibility(self, visibility):
        if visibility:
            self.show()
        else:
            self.hide()

    def set_slot(self, slot):
        self.slot = slot
        self.update_()

    def set_anim(self, anim):
        self.set_tag(anim)
        self.update_()

    def set_character(self, character):
        self.char_id = character
        if character == 0:
            self.hide()
            return
        load_animation(f"data_lt2/ani/eventchr/chr{character}.arc", self)
        try:
            load_animation(f"data_lt2/ani/sub/chr{character}_face.arc", self.character_mouth)
        except:
            self.character_mouth.kill()
        self.set_tag_by_num(1)
        self.update_()
        self.show()

    def get_anim_list(self):
        return list(map(lambda tag: tag["name"], self.sprite_sheet_info["meta"]["frameTags"]))

    def set_talking(self):
        current_tag = self.current_tag["name"]
        if not current_tag.startswith("*"):
            self.set_tag("*" + current_tag)
            if self.current_tag["name"] != "*" + current_tag:
                self.set_tag("*" + current_tag + " ")
            self.update_()

    def set_not_talking(self):
        current_tag = self.current_tag["name"]
        if current_tag.endswith(" "):
            current_tag = current_tag[:-1]
        if current_tag.startswith("*"):
            self.set_tag(current_tag[1:])
            self.update_()

    def get_char_id(self):
        return self.char_id

    def __str__(self):
        return f"<Character {self.char_id}>"
