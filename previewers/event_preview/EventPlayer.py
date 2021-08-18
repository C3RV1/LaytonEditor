import formats.event as ev_dat
import PygameEngine.GameManager
import PygameEngine.Input
import PygameEngine.Sprite
import PygameEngine.UI.UIManager
import pygame_utils.sound.SADLStreamPlayer
from previewers.event_preview.EventCharacter import EventCharacter
from previewers.event_preview.EventDialogue import EventDialogue
from pygame_utils import TwoScreenRenderer
from pygame_utils.rom import RomSingleton
from pygame_utils.rom.rom_extract import load_animation
from .EventBG import EventBG
from previewers.event_preview.abstracts.EventCommands import *
from .EventSound import EventSound
from .EventWaiter import EventWaiter


class EventPlayer(TwoScreenRenderer.TwoScreenRenderer):
    def __init__(self, event_id=None):
        super(EventPlayer, self).__init__()
        self.event_id = event_id

        self.inp = PygameEngine.Input.Input()

        self.event_data = ev_dat.Event(rom=RomSingleton.RomSingleton().rom)

        self.top_bg = EventBG(self.top_group, "top")
        self.btm_bg = EventBG(self.btm_group, "bottom")

        self.characters = []

        self.current_gds_command = 0
        self.waiter = EventWaiter()

        self.sound_player = EventSound()

        self.dialogue: EventDialogue = EventDialogue(self.btm_group, self)
        self.dialogue.layer = 100
        self.dialogue.draw_alignment[1] = self.dialogue.ALIGNMENT_TOP
        self.dialogue.world_rect.y += 192 // 2
        self.ui_manager.add(self.dialogue)

        self.commands = []

        self.run_events = False

    def start_bg_music(self):
        pass
        # Plays the bg music of the room you where in (BG_004 for testing)
        # self.sound_player.play_smdl(f"data_lt2/sound/BG_004.SMD")

    def reset(self):
        self.sound_player.stop_sadl()
        self.sound_player.stop_smdl()
        self.waiter.stop()
        self.dialogue.end_dialogue()

        self.current_gds_command = 0

    def set_event_id(self, ev_id):
        self.event_id = ev_id
        self.event_data.set_event_id(ev_id)
        self.event_data.load_from_rom()

    def load(self, skip_fade_in=False):
        super().load()
        self.reset()
        self.start_bg_music()

        self.top_bg.add(self.top_group)
        self.top_bg.load()
        self.btm_bg.add(self.btm_group)
        self.btm_bg.load()
        self.btm_bg.fade(self.btm_bg.FADE_IN, 0, True)
        self.top_group.add([])
        for character in self.characters:
            self.btm_group.add(character)

        if self.event_id is None:
            raise ValueError("event_id can't be none")
        self.event_data.set_event_id(self.event_id)
        self.event_data.load_from_rom()

        while len(self.characters) < 6:
            self.characters.append(EventCharacter(self.btm_group))

        self.commands = event_to_commands(self.event_data, bg_btm=self.btm_bg,
                                          bg_top=self.top_bg, character_obj=self.characters,
                                          sound_player=self.sound_player, waiter=self.waiter,
                                          dialogue=self.dialogue)
        load_animation(f"data_lt2/ani/event/twindow.arc", self.dialogue)
        self.dialogue.init_position()
        self.run_gds_command()

    def unload(self):
        super(EventPlayer, self).unload()
        self.sound_player.stop_sadl()
        self.sound_player.stop_smdl()
        self.top_bg.unload()
        self.btm_bg.unload()
        for character in self.characters:
            character.unload()
        self.dialogue.unload()

    def update(self):
        super().update()
        if self.inp.quit:
            self.running = False

        # Update character animations
        for character in self.characters:
            if character.char_id == 0:
                continue
            character.update_animation(self.gm.delta_time)
            if character.character_mouth is not None:
                character.character_mouth.update_animation(self.gm.delta_time)

        # Update faders and shakers
        self.top_bg.update_()
        self.btm_bg.update_()

        # Update sounds
        self.sound_player.update_()
        self.dialogue.update_()

        # Update wait
        self.waiter.update_()

        # Update UI Elements
        self.ui_manager.update()

        if not self.is_busy() and self.run_events:
            self.run_gds_command()

    def run_gds_command(self, run_until_command=-1):
        self.run_events = run_until_command == -1  # Should we play commands
        if not self.run_events:
            Debug.log_debug(f"Running until command {run_until_command}", self)
        while True:
            if self.current_gds_command >= len(self.commands):
                self.run_events = False
                break
            next_command: EventCMD = self.commands[self.current_gds_command]

            # If we have completed run_until_command and we are auto_progressing to next command
            if self.current_gds_command > run_until_command and not self.run_events:
                return
            self.current_gds_command += 1

            # Have we completed run_until_command?
            editing = not self.run_events
            instant = (self.current_gds_command <= run_until_command)

            try:
                next_command.execute(editing, instant)
            except Exception as e:
                Debug.log_error(f"Error while executing command. Error {e}", self)

            # If we should return and we are auto_progressing to next command
            if self.is_busy() and not instant:
                return
        Debug.log("Event execution finished", self)

    def is_busy(self):
        return self.top_bg.busy() or self.btm_bg.busy() or self.waiter.busy() or self.dialogue.busy()

    def exit(self):
        super().exit()

    def execute_command(self, command):
        command_split = command.split(" ")
        if command_split[0] == "setani":
            try:
                int(command_split[1])
            except:
                Debug.log_warning(f"Command setani 1: Cannot set for character {command_split[1]}", self)
                return
            character = None
            for char in self.characters:
                char: EventCharacter
                if char.get_char_id() == int(command_split[1]):
                    character = char
                    break
            if character:
                character.set_anim(command_split[2].replace("_", " "))
                Debug.log(f"Command setani: Setting {character} to {command_split[2].replace('_', ' ')}", self)
            else:
                Debug.log_warning(f"Command setani 2: Cannot set for character {command_split[1]}", self)
