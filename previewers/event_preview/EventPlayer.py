from typing import List, Optional

import pg_engine as pge
from formats import gds
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
        self.next_voice = -1
        self.next_dialogue_sfx = -1

        self.sprite_loader = RomSingleton().get_sprite_loader()
        self.font_loader = RomSingleton().get_font_loader()

        self.top_bg = EventBG("top")
        self.sprite_loader.load(f"data_lt2/bg/event/sub{self.event.map_top_id}.arc", self.top_bg.bg,
                                sprite_sheet=False)
        self.top_bg.fade(2, None, True)
        self.top_bg.set_opacity(0)
        self.btm_bg = EventBG("btm")
        self.sprite_loader.load(f"data_lt2/bg/map/main{self.event.map_bottom_id}.arc", self.btm_bg.bg,
                                sprite_sheet=False)
        self.btm_bg.set_opacity(120)
        self.btm_bg.fade(2, None, True)

        self.waiter = EventWaiter()
        self.event_sound = EventSound()

        self.characters: List[Optional[EventCharacter]] = [None]*8

        for i in range(8):
            if self.event.characters[i] == 0:
                continue
            char_id = self.event.characters[i]
            slot = self.event.characters_pos[i]
            anim = self.event.characters_anim_index[i]
            visibility = self.event.characters_shown[i]
            char = EventCharacter(char_id, slot, anim, visibility, self.sprite_loader)
            self.characters[i] = char

        self.dialogue = EventDialogue(self, position=[0, 192//2 + 3],
                                      center=[pge.Alignment.CENTER, pge.Alignment.BOTTOM])
        self.sprite_loader.load("data_lt2/ani/event/twindow.ani", self.dialogue)
        self.dialogue.init_text(self.font_loader)

        self.run_events_until_busy()

    def run_events_until_busy(self):
        while True:
            if self.current_command >= len(self.event.event_gds.commands):
                return
            command = self.event.event_gds.commands[self.current_command]
            self.current_command += 1

            self.execute_gds_command(command)

            if self.is_busy():
                return

    def execute_gds_command(self, command: gds.GDSCommand):
        fade_out = 1
        fade_in = 2
        if command.command == 0x2:
            self.top_bg.fade(fade_in, None, False)
            self.btm_bg.fade(fade_in, None, False)
        elif command.command == 0x3:
            self.top_bg.fade(fade_out, None, False)
            self.btm_bg.fade(fade_out, None, False)
        elif command.command == 0x4:
            dialogue_gds = self.event.get_text(command.params[0])
            if len(dialogue_gds.params) != 5:
                return
            character = None
            for char in self.characters:
                if char.get_char_id() == dialogue_gds.params[0]:
                    character = char
                    break
            self.dialogue.start_dialogue(character, dialogue_gds.params[1], dialogue_gds.params[4], self.next_voice,
                                         self.next_dialogue_sfx, self.sprite_loader)
            self.next_voice = -1
            self.next_dialogue_sfx = -1
        elif command.command == 0x21:
            bg_path = command.params[0]
            self.sprite_loader.load(f"data_lt2/bg/{bg_path}", self.btm_bg.bg, sprite_sheet=False)
            self.btm_bg.set_opacity(0)
        elif command.command == 0x22:
            bg_path = command.params[0]
            self.sprite_loader.load(f"data_lt2/bg/{bg_path}", self.top_bg.bg, sprite_sheet=False)
            self.top_bg.set_opacity(0)
        elif command.command == 0x2a:
            self.characters[command.params[0]].show()
        elif command.command == 0x2b:
            self.characters[command.params[0]].hide()
        elif command.command == 0x2c:
            # Still not clue about why it works like this
            if command.params[0] < 8:
                self.characters[command.params[0]].set_visibility(command.params[1] > 0)
        elif command.command == 0x30:
            self.characters[command.params[0]].set_slot(command.params[1])
        elif command.command == 0x31:
            self.waiter.wait(command.params[0])
        elif command.command == 0x32:
            self.btm_bg.fade(fade_in, None, False)
        elif command.command == 0x33:
            self.btm_bg.fade(fade_out, None, False)
        elif command.command == 0x37:
            self.btm_bg.set_opacity(command.params[3])
        elif command.command == 0x3f:
            character = None
            for char in self.characters:
                if char.get_char_id() == command.params[0]:
                    character = char
                    break
            if character:
                character.set_anim(command.params[1])
        elif command.command == 0x5c:
            self.next_voice = command.params[0]
        elif command.command == 0x5d:
            self.event_sound.play_sadl(f"data_lt2/stream/ST_{str(command.params[0]).zfill(3)}.SAD")
        elif command.command == 0x62:
            self.event_sound.play_smdl(f"data_lt2/sound/BG_{str(command.params[0]).zfill(3)}.SMD")
        elif command.command == 0x6a:
            self.btm_bg.shake()
        elif command.command == 0x72:
            self.top_bg.fade(fade_out, command.params[0], False)
            self.btm_bg.fade(fade_out, command.params[0], False)
        elif command.command == 0x80:
            self.top_bg.fade(fade_in, command.params[0], False)
            self.btm_bg.fade(fade_in, command.params[0], False)
        elif command.command == 0x87:
            self.top_bg.fade(fade_out, command.params[0], False)
        elif command.command == 0x88:
            self.top_bg.fade(fade_in, command.params[0], False)
        elif command.command == 0x8a:
            self.event_sound.fade(False, command.params[1])
        elif command.command == 0x8b:
            self.event_sound.fade(True, command.params[0])
        elif command.command == 0x99:
            self.next_dialogue_sfx = command.params[0]
        else:
            pge.Debug.log_warning(f"Command {hex(command.command)} not recognised (skipped). ", self)

    def execute_str_command(self, command):
        print(command)
        command_split = command.split(" ")
        if command_split[0] == "setani":
            try:
                int(command_split[1])
            except ValueError:
                return
            character = None
            for char in self.characters:
                char: EventCharacter
                if char.get_char_id() == int(command_split[1]):
                    character = char
                    break
            if character:
                character.set_anim(command_split[2].replace("_", " "))

    def update(self, dt: float):
        self.waiter.update_(dt)
        self.event_sound.update_(dt)
        self.top_bg.update_(dt)
        self.btm_bg.update_(dt)
        self.dialogue.interact(self.btm_camera, dt)
        for character in self.characters:
            if character:
                character.animate(dt)
        if not self.is_busy():
            self.run_events_until_busy()

    def draw(self):
        self.top_bg.draw_back(self.top_camera)
        self.top_bg.draw_front(self.top_camera)

        self.btm_bg.draw_back(self.btm_camera)
        for character in self.characters:
            if character:
                character.draw(self.btm_camera)
        self.dialogue.draw(self.btm_camera)
        self.btm_bg.draw_front(self.btm_camera)

    def unload(self):
        self.top_bg.unload()
        self.btm_bg.unload()
        for character in self.characters:
            if character:
                character.unload()
        self.dialogue.unload()
        self.event_sound.stop_smdl()
        self.event_sound.stop_sadl()

    def is_busy(self):
        return self.top_bg.busy() or self.btm_bg.busy() or self.waiter.busy() or self.dialogue.busy()
