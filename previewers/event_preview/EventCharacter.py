import pg_engine as pge


class EventCharacter(pge.Sprite):
    FACING_LEFT = 1
    FACING_RIGHT = 2

    SLOT_MAX = 6
    SLOT_OFFSET = {0: 0, 1: 52*2 - 30,
                   2: 0, 3: 0,
                   4: 52, 5: 52,
                   6: 0}
    SLOT_ON_LEFT = [0, 3, 4]  # Verified against game binary
    SLOT_ON_RIGHT = [1, 2, 5, 6]

    def __init__(self, character_id, slot, anim_num, visibility, loader, *args, **kwargs):
        super(EventCharacter, self).__init__(*args, **kwargs)
        self.orientation = EventCharacter.FACING_RIGHT
        self.center[1] = pge.Alignment.BOTTOM
        self.position[1] = 192 // 2
        self.slot = slot
        self.character_mouth: pge.Sprite = pge.Sprite()

        self.char_id = character_id

        self.talking = False

        self.load_character(loader)
        self.set_tag_by_num(anim_num)
        self.set_visibility(visibility)

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
            self.center[0] = pge.Alignment.LEFT
        else:
            offset = (256 // 2) - EventCharacter.SLOT_OFFSET[self.slot]
            self.center[0] = pge.Alignment.RIGHT
        self.position[0] = offset
        self.update_child()

    def update_child(self):
        mouth_offset = [self._active_tag.vars_["child_x"], self._active_tag.vars_["child_y"]]
        world_rect = self.get_world_rect()
        if self.character_mouth is not None:
            if self.orientation == EventCharacter.FACING_RIGHT:
                mouth_offset[0] = world_rect.w - mouth_offset[0]
                self.character_mouth.center[0] = pge.Alignment.RIGHT
                self.character_mouth.flipped = [True, False]
            else:
                self.character_mouth.center[0] = pge.Alignment.LEFT
                self.character_mouth.flipped = [False, False]

            self.character_mouth.position[0] = world_rect.x + mouth_offset[0]
            self.character_mouth.position[1] = self.position[1] - world_rect.h + mouth_offset[1]
            self.character_mouth.center[1] = pge.Alignment.TOP
            self.character_mouth.set_tag_by_num(self._active_tag.vars_["child_index"])
            if self._active_tag.vars_["child_index"] == 0:
                self.character_mouth.visible = False
            elif self.visible and not self.character_mouth.visible:
                self.character_mouth.visible = True

    def show(self):
        if not self.visible:
            self.visible = True
            if self.character_mouth is not None:
                self.character_mouth.visible = True

    def hide(self):
        if self.visible:
            self.visible = False
            if self.character_mouth is not None:
                self.character_mouth.visible = False

    def set_visibility(self, visibility):
        if visibility:
            self.show()
        else:
            self.hide()

    def set_slot(self, slot):
        self.slot = slot

    def set_anim(self, anim: str):
        anim = anim.replace("surprise", "suprise")
        self.set_tag(anim)
        if self.talking:
            self.set_talking()
        else:
            self.set_not_talking()

    def load_character(self, loader: pge.SpriteLoader):
        if loader:
            loader.load(f"data_lt2/ani/eventchr/chr{self.char_id}.arc", self, sprite_sheet=True)
        if (drawoff := self.vars.get("drawoff", None)) is not None:
            self.position[0] += drawoff[0]
            self.position[1] += drawoff[1]
        if self.vars.get('child_image', "") != "" and loader:
            loader.load(f"data_lt2/ani/sub/{self.vars['child_image']}", self.character_mouth, sprite_sheet=True)
        self.set_tag_by_num(1)

    def animate(self, dt: float):
        super(EventCharacter, self).animate(dt)
        if self.character_mouth:
            self.character_mouth.animate(dt)

    def set_talking(self):
        self.talking = True
        current_tag = self._active_tag.name
        if not current_tag.startswith("*"):
            self.set_tag("*" + current_tag)
            if self._active_tag.name != "*" + current_tag:
                self.set_tag("*" + current_tag + " ")

    def set_not_talking(self):
        self.talking = False
        current_tag = self._active_tag.name
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

    def draw(self, cam: pge.Camera):
        super(EventCharacter, self).draw(cam)
        self.character_mouth.draw(cam)

    def get_visibility(self):
        return self.visible
