from typing import List, Optional

from formats.event import Event
from .EventCharacter import EventCharacter
from .EventBG import EventBG
from .EventSound import EventSound
from .EventWaiter import EventWaiter
from .EventDialogue import EventDialogue
from pg_utils.rom.RomSingleton import RomSingleton
from pg_utils.TwoScreenRenderer import TwoScreenRenderer


class EventPlayer(TwoScreenRenderer):
    def __init__(self, event: Event):
        super(EventPlayer, self).__init__()
        self.event = event
        self.current_command = 0

        self.sprite_loader = RomSingleton().get_sprite_loader()
        self.font_loader = RomSingleton().get_font_loader()

        self.top_bg = EventBG("top")
        self.sprite_loader.load(f"data_lt2/bg/event/sub{self.event.map_top_id}.arc", self.top_bg, sprite_sheet=False)
        self.btm_bg = EventBG("btm")
        self.sprite_loader.load(f"data_lt2/bg/map/main{self.event.map_bottom_id}.arc", self.btm_bg, sprite_sheet=False)

        self.waiter = EventWaiter()
        self.event_sound = EventSound()

        self.characters: List[Optional[EventCharacter]] = [None]*8
        self.character_slots: List[Optional[EventCharacter]] = [None]*6

        for i in range(8):
            if self.event.characters[i] == 0:
                continue
            char_id = self.event.characters[i]
            slot = self.event.characters_pos[i]
            anim = self.event.characters_anim_index[i]
            visibility = self.event.characters_shown[i]
            char = EventCharacter(char_id, slot, anim, visibility, self.sprite_loader)
            self.character_slots[slot] = char
            self.characters[i] = char

        self.dialogue = EventDialogue(self)
        self.dialogue.init_text(self.font_loader)

        self.run_events_until_busy()

    def run_events_until_busy(self):
        while True:
            if self.current_command >= len(self.event.event_gds.commands):
                return
            command = self.event.event_gds.commands[self.current_command]
            self.current_command += 1

            # TODO: Process command

            if self.is_busy():
                return

    def update(self, dt: float):
        self.waiter.update_(dt)
        self.event_sound.update_(dt)
        self.top_bg.update_(dt)
        for character in self.character_slots:
            if character:
                character.animate(dt)
        if not self.is_busy():
            self.run_events_until_busy()

    def draw(self):
        self.top_bg.draw_back(self.top_camera)
        self.top_bg.draw_front(self.top_camera)

        self.btm_bg.draw_back(self.btm_camera)
        for character in self.character_slots:
            if character:
                character.draw(self.btm_camera)
        self.btm_bg.draw_front(self.btm_camera)

    def unload(self):
        self.top_bg.unload()
        self.btm_bg.unload()
        for character in self.characters:
            if character:
                character.unload()

    def is_busy(self):
        return self.top_bg.busy() or self.btm_bg.busy() or self.waiter.busy() or self.dialogue.busy()
