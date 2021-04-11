from .EventBGAbstract import EventBGAbstract
from .EventCharacterAbstract import EventCharacterAbstract
from .EventSoundAbstract import EventSoundAbstract
from .EventWaiterAbstract import EventWaiterAbstract
from .EventDialogueAbstract import EventDialogueAbstract
import formats.gds
import formats.event_data
from PygameEngine.Debug import Debug


class EventCMD:
    def __init__(self):
        pass

    def execute(self, editing, instant):
        Debug.log(f"Executing unknown", self)


class LoadCMD(EventCMD):
    def __init__(self, character_obj, characters, characters_shown, characters_pos, characters_anim,
                 top_id, btm_id, bg_top, bg_btm):
        super().__init__()
        self.character_objects = character_obj
        self.characters = characters
        self.characters_shown = characters_shown
        self.characters_pos = characters_pos
        self.characters_anim = characters_anim

        self.top_id = top_id
        self.btm_id = btm_id
        self.bg_top: EventBGAbstract = bg_top
        self.bg_btm: EventBGAbstract = bg_btm

    def execute(self, editing, instant):
        Debug.log(f"Executing load characters={self.characters} anims={self.characters_anim}", self)
        self.setup_characters()
        self.bg_top.set_bg(f"data_lt2/bg/event/sub{self.top_id}.arc")
        self.bg_btm.set_bg(f"data_lt2/bg/map/main{self.btm_id}.arc")
        self.bg_top.set_opacity(0)
        self.bg_btm.set_opacity(120)
        if editing:
            self.bg_top.set_fade_max_opacity(180)
            self.bg_btm.set_fade_max_opacity(180)
        else:
            self.bg_top.set_fade_max_opacity(255)
            self.bg_btm.set_fade_max_opacity(255)

    def setup_characters(self):
        for char_num, char_obj in enumerate(self.character_objects):
            char_obj: EventCharacterAbstract
            char_obj.set_character(self.characters[char_num])
            if self.characters[char_num] == 0:
                continue
            char_obj.set_visibility(self.characters_shown[char_num])
            char_obj.set_slot(self.characters_pos[char_num])
            if isinstance(self.characters_anim[char_num], int):
                self.characters_anim[char_num] = char_obj.get_anim_list()[self.characters_anim[char_num]]
            char_obj.set_anim(self.characters_anim[char_num])


class FadeCMD(EventCMD):
    FADE_OUT = 1
    FADE_IN = 2

    FADE_TOP = 1
    FADE_BTM = 2
    FADE_BOTH = FADE_TOP | FADE_BTM

    def __init__(self, fade_type, fade_screen, bg_top, bg_btm, time):
        super().__init__()
        self.fade_type = fade_type
        self.fade_screen = fade_screen
        self.bg_top: EventBGAbstract = bg_top
        self.bg_btm: EventBGAbstract = bg_btm
        self.fade_frames = time

    def execute(self, editing, instant):
        Debug.log(f"Executing fade screen={self.fade_screen} "
                  f"type={self.fade_type} time={self.fade_frames}", self)
        if self.fade_screen & self.FADE_TOP:
            self.bg_top.fade(self.fade_type, self.fade_frames, instant)
            if editing:
                self.bg_top.set_fade_max_opacity(180)
            else:
                self.bg_top.set_fade_max_opacity(255)
        if self.fade_screen & self.FADE_BTM:
            self.bg_btm.fade(self.fade_type, self.fade_frames, instant)
            if editing:
                self.bg_btm.set_fade_max_opacity(180)
            else:
                self.bg_btm.set_fade_max_opacity(255)


class BGLoadCMD(EventCMD):
    TOP = 0
    BTM = 1

    def __init__(self, bg, bg_top, bg_btm, load_path):
        super().__init__()
        self.bg = bg
        self.bg_top: EventBGAbstract = bg_top
        self.bg_btm: EventBGAbstract = bg_btm
        self.load_path = load_path

    def execute(self, editing, instant):
        Debug.log(f"Executing bg load bg={self.bg} "
                  f"load_path={self.load_path}", self)
        if self.bg == self.TOP:
            self.bg_top.set_bg("data_lt2/bg/" + self.load_path)
        else:
            self.bg_btm.set_bg("data_lt2/bg/" + self.load_path)


class BGOpacityCMD(EventCMD):
    def __init__(self, bg, opacity):
        super().__init__()
        self.bg: EventBGAbstract = bg
        self.opacity = opacity

    def execute(self, editing, instant):
        Debug.log(f"Executing bg opacity bg={self.bg} opacity={self.opacity}", self)
        self.bg.set_opacity(self.opacity)


class BGShakeCMD(EventCMD):
    def __init__(self, bg):
        super().__init__()
        self.bg: EventBGAbstract = bg

    def execute(self, editing, instant):
        Debug.log(f"Executing bg shake bg={self.bg}", self)
        self.bg.shake()


class ChrShowCMD(EventCMD):
    def __init__(self, character):
        super().__init__()
        self.character: EventCharacterAbstract = character

    def execute(self, editing, instant):
        Debug.log(f"Executing chr show character={self.character}", self)
        self.character.show()


class ChrHideCMD(EventCMD):
    def __init__(self, character):
        super().__init__()
        self.character: EventCharacterAbstract = character

    def execute(self, editing, instant):
        Debug.log(f"Executing chr hide character={self.character}", self)
        self.character.hide()


class ChrVisibilityCMD(EventCMD):
    def __init__(self, character, visibility):
        super().__init__()
        self.character: EventCharacterAbstract = character
        self.visibility = visibility

    def execute(self, editing, instant):
        Debug.log(f"Executing chr visibility character={self.character} "
                  f"visibility={self.visibility}", self)
        if self.character:
            self.character.set_visibility(self.visibility)


class ChrSlotCMD(EventCMD):
    def __init__(self, character, next_slot):
        super().__init__()
        self.character: EventCharacterAbstract = character
        self.next_slot = next_slot

    def execute(self, editing, instant):
        Debug.log(f"Executing chr slot character={self.character} "
                  f"slot={self.next_slot}", self)
        self.character.set_slot(self.next_slot)


class ChrAnimCMD(EventCMD):
    def __init__(self, character, next_anim):
        super().__init__()
        self.character: EventCharacterAbstract = character
        self.next_anim = next_anim

    def execute(self, editing, instant):
        Debug.log(f"Executing chr anim character={self.character} "
                  f"anim={self.next_anim}", self)
        self.character.set_anim(self.next_anim)


class SadSfxCMD(EventCMD):
    def __init__(self, player, sad_id):
        super().__init__()
        self.player: EventSoundAbstract = player
        self.sad_id = sad_id

    def execute(self, editing, instant):
        Debug.log(f"Executing sad sfx sad_id={self.sad_id}", self)
        if not instant:
            self.player.play(f"data_lt2/stream/ST_{str(self.sad_id).zfill(3)}.SAD")


class DialogueCMD(EventCMD):
    def __init__(self, dialogue, character, text, anim, voice):
        super().__init__()
        self.dialogue: EventDialogueAbstract = dialogue
        self.character: EventCharacterAbstract = character
        self.text = text
        if anim == "NONE":
            self.anim = None
        else:
            self.anim = anim
        self.voice = voice

    def execute(self, editing, instant):
        Debug.log(f"Executing dialogue character={self.character} anim={self.anim} text={self.text} "
                  f"voice={self.voice}", self)
        self.dialogue.start_dialogue(self.character, self.anim, self.text, self.voice)
        if instant:
            self.dialogue.end_dialogue()


class WaitCMD(EventCMD):
    def __init__(self, waiter, wait_frames):
        super().__init__()
        self.waiter: EventWaiterAbstract = waiter
        self.wait_frames = wait_frames

    def execute(self, editing, instant):
        Debug.log(f"Executing wait frames={self.wait_frames}", self)
        if not instant:
            self.waiter.wait(self.wait_frames)


def event_to_commands(event: formats.event_data.EventData, character_obj, bg_top, bg_btm, waiter, sfx_player,
                      dialogue):
    commands = list()
    commands.append(
        LoadCMD(character_obj, event.characters, list(map(lambda x: x != 0, event.characters_shown)),
                event.characters_pos, event.characters_anim_index,
                event.map_top_id, event.map_bottom_id, bg_top, bg_btm)
    )
    commands[-1].setup_characters()
    next_voice = -1
    for event_gds_cmd in event.event_gds.commands:  # type: formats.gds.GDSCommand
        if event_gds_cmd.command == 0x2:
            commands.append(
                FadeCMD(FadeCMD.FADE_IN, FadeCMD.FADE_BOTH, bg_top, bg_btm, None)
            )
        elif event_gds_cmd.command == 0x3:
            commands.append(
                FadeCMD(FadeCMD.FADE_OUT, FadeCMD.FADE_BOTH, bg_top, bg_btm, None)
            )
        elif event_gds_cmd.command == 0x4:
            dialogue_gds = event.get_text(event_gds_cmd.params[0])
            character = None
            for char in character_obj:
                if char.get_char_id() == dialogue_gds.params[0] and char.get_char_id() != 0:
                    character = char
                    break
            commands.append(
                DialogueCMD(dialogue, character, dialogue_gds.params[4], dialogue_gds.params[1], next_voice)
            )
            next_voice = -1
        elif event_gds_cmd.command == 0x21:
            commands.append(
                BGLoadCMD(BGLoadCMD.BTM, bg_top, bg_btm, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x22:
            commands.append(
                BGLoadCMD(BGLoadCMD.TOP, bg_top, bg_btm, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x2a:
            commands.append(
                ChrShowCMD(character_obj[event_gds_cmd.params[0]])
            )
        elif event_gds_cmd.command == 0x2b:
            commands.append(
                ChrHideCMD(character_obj[event_gds_cmd.params[0]])
            )
        elif event_gds_cmd.command == 0x2c:
            # WTF WHY DOES THIS WORK LIKE THIS
            if event_gds_cmd.params[0] >= len(character_obj):
                character = None
                for char in character_obj:
                    if char.get_char_id() == event_gds_cmd.params[0] and char.get_char_id() != 0:
                        character = char
                        break
            else:
                character = character_obj[event_gds_cmd.params[0]]
            commands.append(
                ChrVisibilityCMD(character, event_gds_cmd.params[1] > 0)
            )
        elif event_gds_cmd.command == 0x30:
            character = None
            for char in character_obj:
                if char.get_char_id() == event_gds_cmd.params[0] and char.get_char_id() != 0:
                    character = char
                    break
            commands.append(
                ChrSlotCMD(character,
                           event_gds_cmd.params[1])
            )
        elif event_gds_cmd.command == 0x32:
            commands.append(
                FadeCMD(FadeCMD.FADE_IN, FadeCMD.FADE_BTM, bg_top, bg_btm, None)
            )
        elif event_gds_cmd.command == 0x33:
            commands.append(
                FadeCMD(FadeCMD.FADE_OUT, FadeCMD.FADE_BTM, bg_top, bg_btm, None)
            )
        elif event_gds_cmd.command == 0x31:
            commands.append(
                WaitCMD(waiter, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x37:
            commands.append(
                BGOpacityCMD(bg_btm, event_gds_cmd.params[3])
            )
        elif event_gds_cmd.command == 0x3f:
            character = None
            for char in character_obj:
                if char.get_char_id() == event_gds_cmd.params[0] and char.get_char_id() != 0:
                    character = char
                    break
            commands.append(
                ChrAnimCMD(character, event_gds_cmd.params[1])
            )
        elif event_gds_cmd.command == 0x5c:
            next_voice = event_gds_cmd.params[0]
        elif event_gds_cmd.command == 0x5d:
            commands.append(
                SadSfxCMD(sfx_player, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x5e and False:
            pass
        elif event_gds_cmd.command == 0x6a:
            commands.append(
                BGShakeCMD(bg_btm)
            )
        elif event_gds_cmd.command == 0x72:
            commands.append(
                FadeCMD(FadeCMD.FADE_OUT, FadeCMD.FADE_BOTH, bg_top, bg_btm, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x80:
            commands.append(
                FadeCMD(FadeCMD.FADE_IN, FadeCMD.FADE_BOTH, bg_top, bg_btm, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x87:
            commands.append(
                FadeCMD(FadeCMD.FADE_OUT, FadeCMD.FADE_TOP, bg_top, bg_btm, event_gds_cmd.params[0])
            )
        elif event_gds_cmd.command == 0x88:
            commands.append(
                FadeCMD(FadeCMD.FADE_IN, FadeCMD.FADE_TOP, bg_top, bg_btm, event_gds_cmd.params[0])
            )
        else:
            Debug.log_warning(f"Command {hex(event_gds_cmd.command)} not recognised (skipped). "
                              f"Event shouldn't be saved.", "GDS to Commands")
    return commands
