import logging

from formats.event import Event
from formats.movie import Movie
from formats.gds import GDSCommand, GDS
from gui.SettingsManager import SettingsManager
from utility.replace_substitutions import replace_substitutions
from formats.dlz import TimeDefinitionsDlz


MAX_TEXT_LENGTH = 50


def parse_fade(command: GDSCommand, **_kwargs):
    fade_in = command.command in [0x2, 0x32, 0x80, 0x81, 0x88]
    fade_time = None
    fade_screens = 0
    if command.command in [0x2, 0x3, 0x72, 0x80]:
        fade_screens = 2  # both screens
    elif command.command in [0x32, 0x33, 0x7f, 0x81]:
        fade_screens = 0  # btm screen
    elif command.command in [0x87, 0x88]:
        fade_screens = 1  # top screen
    if command.command in [0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
        fade_time = command.params[0]  # timed

    screens = {
        0: "Bottom screen",
        1: "Top screen",
        2: "Both screens"
    }[fade_screens]

    duration = "Default frames" if fade_time is None else f"{fade_time} frames"

    return f"Screen: Fade {'In' if fade_in else 'Out'}\n" \
           f"{screens} ({duration})"


def parse_dialogue(command: GDSCommand, event: Event = None, **_kwargs):
    if event is None:
        logging.error("Error: Dialogue event=None???", exc_info=True)
        return "Error: Dialogue event=None???"
    text_id = command.params[0]
    text = event.get_text(text_id)

    char_id = text.params[0]
    if char_id != 0:
        char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")
    else:
        char_name = "Narrator"

    text_parsed = replace_substitutions(text.params[4])

    text_one_line = text_parsed.split('\n')
    if len(text_one_line) > 1 or len(text_one_line[0]) > MAX_TEXT_LENGTH:
        text_one_line = text_one_line[0][:MAX_TEXT_LENGTH] + " [...]"
    else:
        text_one_line = text_one_line[0]

    return f"Dialogue {char_name}: {char_id} [{text.params[1]}, {text.params[2]}] ({text.params[3]} voice pitch)\n" \
           f"{text_one_line}"


def parse_set_mode_id(command: GDSCommand, **_kwargs):
    mode = {
        0x5: "Place",
        0x8: "Movie",
        0x9: "Event",
        0xb: "Puzzle"
    }[command.command]
    return f"Sequencing: Set Mode ID\n" \
           f"{mode} to {command.params[0]}"


def parse_set_mode(command: GDSCommand, **_kwargs):
    mode = {
        "narration": "Narration",
        "movie": "Movie",
        "puzzle": "Puzzle",
        "drama event": "Event",
        "room": "Place",
        "name": "Name",
        "staff": "Staff",
        "nazoba": "Nazoba",
        "menu": "Menu",
        "challenge": "Challenge",
        "sub herb": "Herbal tea",
        "sub camera": "Camera",
        "sub ham": "Hamster",
        "passcode": "Passcode"
    }[command.params[0]]
    return f"Sequencing: {'Next Mode' if command.command == 0x6 else 'Queue Following Mode'}\n" \
           f"Mode: {mode}"


def parse_wait(command: GDSCommand, rom=None, **_kwargs):
    if command.command == 0x31:
        line = f"{command.params[0]} Frames"
    elif command.command == 0x69:
        line = f"Tap"
    elif command.command == 0x6c:
        line = f"Tap or {command.params[0]} Frames"
    else:  # 0x8e
        if rom is None:
            return f"Error: Wait Time Definition rom=None???"
        tm_def = TimeDefinitionsDlz(rom=rom, filename="data_lt2/rc/tm_def.dlz")
        frames = tm_def[command.params[0]]
        line = f"Time Definition {command.params[0]} ({frames} frames)"
    return f"Wait: {line}"


def parse_load_screen(command: GDSCommand, **_kwargs):
    return f"Screen: Load {'Bottom' if command.command == 0x21 else 'Top'} Background\n" \
           f"{command.params[0]}"


def parse_character_visibility(command: GDSCommand, event=None, **_kwargs):
    if event is None:
        logging.error("Error: Character Visibility event=None???", exc_info=True)
        return "Error: Character Visibility event=None???"
    if command.command in [0x2a, 0x2b]:
        show = command.command == 0x2a
    else:
        show = command.params[1] > 0
    alpha = "" if command.command != 0x2c else ' (alpha)'

    char_id = event.characters[command.params[0]]
    char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")

    return f"Character {char_name}: {char_id} Visibility\n" \
           f"{'Show' if show else 'Hide'}{alpha}"


def parse_chapter(command: GDSCommand, **kwargs):
    return f"Screen: Show Chapter {command.params[0]}"


def parse_character_slot(command: GDSCommand, event=None, **_kwargs):
    if event is None:
        logging.error("Error: Character Slot event=None???", exc_info=True)
        return "Error: Character Slot event=None???"
    char_id = event.characters[command.params[0]]
    char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")

    slot_name = {
        0: "Left 1",
        1: "Center (looking right)",
        2: "Right 1",
        3: "Left 2",
        4: "Left Center",
        5: "Right Center",
        6: "Right 2"
    }[command.params[1]]

    return f"Character {char_name}: {char_id} Slot\n" \
           f"Moving to slot {slot_name}"


def parse_bottom_tint(command: GDSCommand, **_kwargs):
    return f"Screen: Set Bottom Tint (RGBA: {command.params})"


def parse_character_animation(command: GDSCommand, **_kwargs):
    char_id = command.params[0]
    char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")

    return f"Character {char_name}: {char_id} Animation\n" \
           f"Setting animation to {command.params[1]}"


def parse_voice_clip(command: GDSCommand, **_kwargs):
    return f"Audio: Set Voice Clip {command.params[0]}"


def parse_sound_effect(command: GDSCommand, **_kwargs):
    return f"Audio: Sound Effect {command.params[0]} ({'SAD' if command.command == 0x5d else 'SED'})"


def parse_play_music(command: GDSCommand, **_kwargs):
    if command.command == 0x62:
        return f"Audio: Play Music {command.params[0]} at {command.params[1]} Volume\n" \
               f"Fade In {command.params[2]} Frames"
    else:
        return f"Audio: Play Music {command.params[0]} at {command.params[1]} Volume\n" \
               f"Variation Command? (0x8c)"


def parse_shake_screen(command: GDSCommand, **_kwargs):
    return f"Screen: Shake {'Bottom' if command.command == 0x6a else 'Top'}\n" \
           f"Unk0: {command.params[0]}"


def parse_unlock_journal(command: GDSCommand, **_kwargs):
    return f"Progression: Unlocking Journal {command.params[0]}"


def parse_mystery(command: GDSCommand, **_kwargs):
    return f"Progression: {'Reveal' if command.command == 0x71 else 'Solve'} Mystery {command.params[0]}"


def parse_tea(command: GDSCommand, **_kwargs):
    return f"Minigame: Start Tea\n" \
           f"Hint ID: {command.params[0]}, Solution ID: {command.params[1]}"


def parse_send_to_granny_riddleton(command: GDSCommand, **_kwargs):
    return f"Progression: Send Puzzles to Granny Riddleton\n" \
           f"Puzzle Group: {command.params[0]}"


def parse_item(command: GDSCommand, **_kwargs):
    return f"Progression: {'Pick Up' if command.command == 0x77 else 'Remove'} Item {command.params[0]}"


def parse_progress_prompt(command: GDSCommand, **_kwargs):
    return f"Progression: Save Progress Prompt\n" \
           f"Next Event: {command.params[0]}"


def parse_unlock_minigame(command: GDSCommand, **_kwargs):
    return f"Progression: Unlocking Minigame {command.params[0]}"


def parse_character_shake(command: GDSCommand, event=None, **_kwargs):
    char_id = event.characters[command.params[0]]
    char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")
    return f"Character {char_name}: {char_id} Shake\n" \
           f"Duration?: {command.params[1]}"


def parse_flash_bottom(_command: GDSCommand, **_kwargs):
    return "Screen: Flash Bottom Screen"


def parse_stop_train_sound(_command: GDSCommand, **_kwargs):
    return "Audio: Stop Train Sound"


def parse_music_fade(command: GDSCommand, rom=None, **_kwargs):
    tm_def = TimeDefinitionsDlz(rom=rom, filename="data_lt2/rc/tm_def.dlz")
    frames = tm_def[command.params[1]]
    return f"Audio: Fade Music {'Out' if command.command == 0x8a else 'In'}\n" \
           f"In Time Definition {command.params[1]} ({frames} frames)"


def parse_companion(command: GDSCommand, **_kwargs):
    return f"Progression: {'Add' if command.command == 0x96 else 'Remove'} Companion {command.params[0]}"


def parse_play_train_sound(command: GDSCommand, **_kwargs):
    text = "Audio: Play train sound"
    if command.params[0] != 100:
        text += f"\nStrange Unk0: {command.params[0]}!"
    return text


def parse_movie_subtitle(command: GDSCommand, movie=None, **_kwargs):
    if movie is None:
        logging.error("Error: Movie Subtitle movie=None???", exc_info=True)
        return "Error: Movie Subtitle movie=None???"
    text = movie.subtitles[command.params[0]].split("\n")
    if len(text) > 1 or len(text[0]) > MAX_TEXT_LENGTH:
        text = text[0][:MAX_TEXT_LENGTH] + " [...]"
    else:
        text = text[0]
    return f"Movie: Subtitle from {command.params[1]:.2f}s to {command.params[2]:.2f}s\n" \
           f"{text}"


def parse_complete_game(_command: GDSCommand, **_kwargs):
    return "Progression: Complete Game"


event_cmd_parsers = (
    ((0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88), parse_fade),
    ((0x4,), parse_dialogue),
    ((0x5, 0x8, 0x9, 0xb), parse_set_mode_id),
    ((0x6, 0x7), parse_set_mode),
    ((0x31, 0x69, 0x6c, 0x8e), parse_wait),
    ((0x21, 0x22), parse_load_screen),
    ((0x2a, 0x2b, 0x2c), parse_character_visibility),
    ((0x2d,), parse_chapter),
    ((0x30,), parse_character_slot),
    ((0x37,), parse_bottom_tint),
    ((0x3f,), parse_character_animation),
    ((0x5c,), parse_voice_clip),
    ((0x5d, 0x5e), parse_sound_effect),
    ((0x62, 0x8c), parse_play_music),
    ((0x6a, 0x6b), parse_shake_screen),
    ((0x70,), parse_unlock_journal),
    ((0x71, 0x7d), parse_mystery),
    ((0x73,), parse_tea),
    ((0x76,), parse_send_to_granny_riddleton),
    ((0x77, 0x7a), parse_item),
    ((0x79,), parse_unlock_minigame),
    ((0x7b,), parse_progress_prompt),
    ((0x7e,), parse_character_shake),
    ((0x82,), parse_flash_bottom),
    ((0x89,), parse_stop_train_sound),
    ((0x8a, 0x8b), parse_music_fade),
    ((0x96, 0x97), parse_companion),
    ((0x9f,), parse_play_train_sound),
    ((0xa1,), parse_complete_game),
)


script_cmd_parsers = (
    ((0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88), parse_fade),
    ((0x5, 0x8, 0x9, 0xb), parse_set_mode_id),
    ((0x6, 0x7), parse_set_mode),
    ((0x31, 0x69, 0x6c, 0x8e), parse_wait),
    ((0x21, 0x22), parse_load_screen),
    ((0x2d,), parse_chapter),
    ((0x37,), parse_bottom_tint),
    ((0x5d, 0x5e), parse_sound_effect),
    ((0x62, 0x8c), parse_play_music),
    ((0x6a, 0x6b), parse_shake_screen),
    ((0x70,), parse_unlock_journal),
    ((0x71, 0x7d), parse_mystery),
    ((0x73,), parse_tea),
    ((0x76,), parse_send_to_granny_riddleton),
    ((0x77, 0x7a), parse_item),
    ((0x79,), parse_unlock_minigame),
    ((0x7b,), parse_progress_prompt),
    ((0x82,), parse_flash_bottom),
    ((0x89,), parse_stop_train_sound),
    ((0x8a, 0x8b), parse_music_fade),
    ((0x96, 0x97), parse_companion),
    ((0xa1,), parse_complete_game),
)

movie_cmd_parsers = (
    ((0xa2,), parse_movie_subtitle),
)


class CommandFactory:
    def __init__(self, command: int, parameters: tuple):
        self.command: int = command
        self.parameters: tuple = parameters

    def create(self, **kwargs):
        return GDSCommand(self.command, list(self.parameters))


class DialogueCommandFactory(CommandFactory):
    def __init__(self):
        super().__init__(0x4, tuple())

    def create(self, event: Event = None, **kwargs):
        if event is None:
            logging.error("Error: DialogueCommandFactory event=None???", exc_info=True)
            return None
        text_index = 100
        while text_index in event.texts:
            text_index += 100
        event.texts[text_index] = GDS(params=[0, "NONE", "NONE", 2, ""])
        return GDSCommand(0x4, [text_index])


class SubtitleCommandFactory(CommandFactory):
    def __init__(self):
        super().__init__(0xa2, tuple())

    def create(self, movie: Movie = None, **kwargs):
        if movie is None:
            logging.error("Error: SubtitleCommandFactory movie=None???", exc_info=True)
            return None
        sub_index = 0
        while sub_index in movie.subtitles:
            sub_index += 1
        movie.subtitles[sub_index] = ""
        return GDSCommand(0xa2, [sub_index, 0.0, 0.0])


event_cmd_context_menu = [
    ("Screen", (
        ("Fade", CommandFactory(0x2, tuple())),
        ("Load Background", CommandFactory(0x21, ("", 3))),
        ("Show Chapter", CommandFactory(0x2d, (1,))),
        ("Set Bottom Tint", CommandFactory(0x37, (15, 5, 0, 120))),
        ("Shake", CommandFactory(0x6a, (30,))),
        ("Flash Bottom", CommandFactory(0x82, tuple()))
    )),
    ("Dialogue", DialogueCommandFactory()),
    ("Character", (
        ("Set Visibility", CommandFactory(0x2a, (0,))),
        ("Set Slot", CommandFactory(0x30, (0, 0))),
        ("Set Animation", None),
        ("Shake", CommandFactory(0x7e, (0, 10)))
    )),
    ("Sequencing", (
        ("Set Mode", CommandFactory(0x6, ("puzzle",))),
        ("Set Mode ID", CommandFactory(0x5, (0,)))
    )),
    ("Wait", CommandFactory(0x69, tuple())),
    (None, None),
    ("Audio", (
        ("Sound Effect", CommandFactory(0x5d, (0,))),
        ("Stop Train Sound", CommandFactory(0x89, tuple())),
        ("Play Train Sound", CommandFactory(0x9f, (100,))),
        ("Play Music", CommandFactory(0x62, (0, 1.0, 0))),
        ("Fade Music", CommandFactory(0x8a, (0.0, 0))),
        ("Voice Clip", CommandFactory(0x5c, (0,)))
    )),
    ("Progression", (
        ("Unlock Journal", CommandFactory(0x70, (0,))),
        ("Reveal/Solve Mystery", CommandFactory(0x71, (1,))),
        ("Send Puzzles to Granny Riddleton", CommandFactory(0x76, (1,))),
        ("Pick Up/Remove Item", CommandFactory(0x77, (0,))),
        ("Save Progress Prompt", CommandFactory(0x7b, (0,))),
        ("Unlock Minigame", CommandFactory(0x79, (0,))),
        ("Companion", CommandFactory(0x96, (1,))),
        ("Complete Game", CommandFactory(0xa1, tuple()))
    ))
]
if SettingsManager().advanced_mode:
    event_cmd_context_menu.append(
        ("Unknown (Dangerous!)", CommandFactory(0x0, tuple()))
    )


script_cmd_context_menu = [
    ("Screen", (
        ("Fade", CommandFactory(0x2, tuple())),
        ("Load Background", CommandFactory(0x21, ("", 3))),
        ("Shake", CommandFactory(0x6a, (30,))),
        ("Flash Bottom", CommandFactory(0x82, tuple()))
    )),
    ("Wait", CommandFactory(0x69, tuple()))
]
if SettingsManager().advanced_mode:
    script_cmd_context_menu.append(
        ("Unknown (Dangerous!)", CommandFactory(0x0, tuple()))
    )


movie_cmd_context_menu = [
    ("Movie Subtitle", SubtitleCommandFactory())
]
if SettingsManager().advanced_mode:
    movie_cmd_context_menu.append(
        ("Unknown (Dangerous!)", CommandFactory(0x0, tuple()))
    )
