from formats.parsers.gds_parsers import EventGDSParser
from .dcc import DCCParser
import re


def split_quoted(data: str, separator=" ", remove_quotes=True):
    split = [""]
    in_quotes = False
    current_separator = ''
    escape = False
    for char in data:
        if char == separator and not in_quotes:
            split.append("")
        elif (char == '"' or char == "(") and not escape and not in_quotes:
            in_quotes = True
            current_separator = '"' if char == '"' else ')'
            if not remove_quotes:
                split[-1] += char
        elif char == current_separator and not escape and in_quotes:
            in_quotes = False
            if not remove_quotes:
                split[-1] += char
        elif char == "\\" and in_quotes and not escape:
            escape = True
            if not remove_quotes:
                split[-1] += char
        else:
            split[-1] += char
            escape = False
    return split


def match_syntax(split, syntax, optional=()):
    for i in range(len(optional) + 1):
        if len(split) == len(syntax) + sum(map(lambda x: len(x), optional[:i])):
            optional_count = i
            break
    else:
        return False

    def flatten(arr):
        a = []
        for b in arr:
            for c in b:
                a.append(c)
        return tuple(a)

    for v1, v2 in zip(split, syntax + flatten(optional[:optional_count])):
        if v2 is None:
            continue
        if isinstance(v2, str):
            if v1 != v2:
                return False
        elif isinstance(v2, list) or isinstance(v2, tuple):
            if v1 not in v2:
                return False
    return True


class EventScriptParser:
    def __init__(self, data: str, ev=None):
        self.ev = ev
        if self.ev is None:
            from ..event import Event
            self.ev = Event()

        self.lines = data.split("\n")
        self.line_num = 0
        self.mode = 0
        self.character_num = 0
        self.defined_characters = []
        self.text_gds_number = 100

    def get_line(self):
        r = self.lines[0]
        self.lines = self.lines[1:]
        self.line_num += 1
        return r

    def peek_line(self):
        if self.lines:
            return self.lines[0]
        else:
            return ""

    def parse(self):
        self.ev.texts = {}
        self.ev.gds.commands = []
        while self.lines:
            line: str = self.get_line()
            if line == "":
                continue
            if match := re.match("-- (.+) --", line):
                mode_str = match.group(1)
                if mode_str == "setup":
                    self.mode = 0
                elif mode_str == "script":
                    self.mode = 1
                else:
                    raise SyntaxError(f"Mode {mode_str} not recognized (line {self.line_num})")
                continue
            if self.mode == 0:  # Setup
                self.setup_mode(line)
            elif self.mode == 1:  # Script
                self.script_mode(line)

    def setup_mode(self, line):
        line_split = split_quoted(line)
        if line_split[0] == "set":
            field = line_split[1]
            try:
                value = int(line_split[2])
            except ValueError:
                raise TypeError(f"Set: Invalid value (line {self.line_num})")
            if field == "top image":
                self.ev.map_top_id = value
            elif field == "bottom image":
                self.ev.map_bottom_id = value
            else:
                raise SyntaxError(f"Field {field} not recognized (line {self.line_num})")
        elif line_split[0] == "character":
            if not match_syntax(line_split,
                                ("character", None, "with", "id", None, "slot", None, "animation", None,
                                 ("is", "isn't"), "visible")):
                raise SyntaxError(f"Character does not match syntax (line {self.line_num})")
            if len(self.defined_characters) == 8:
                raise ValueError(f"More than 8 characters defined (line {self.line_num})")
            name = line_split[1]
            try:
                cid = int(line_split[4])
                slot = int(line_split[6])
                animation = int(line_split[8])
            except ValueError:
                raise TypeError(f"Character: Values do not match types (line {self.line_num})")
            visibility = True if line_split[9] == "is" else False
            self.defined_characters.append(name)
            self.ev.characters[len(self.defined_characters) - 1] = cid
            self.ev.characters_pos[len(self.defined_characters) - 1] = slot
            self.ev.characters_anim_index[len(self.defined_characters) - 1] = animation
            self.ev.characters_shown[len(self.defined_characters) - 1] = visibility
        else:
            raise SyntaxError(f"Unknown setup mode syntax (line {self.line_num})")

    def script_mode(self, line):
        line_split = split_quoted(line)
        event_gds_parser = EventGDSParser(ev=self.ev)
        if line_split[0] == "fade":
            if not match_syntax(line_split, ("fade", ("in", "out"), ("bottom", "btm", "top", "both")),
                                (("in", None, ("frames", "seconds")),)):
                raise SyntaxError(f"Fade does not match syntax (line {self.line_num})")
            fade_in = True if line_split[1] == "in" else False
            fade_screen = {"bottom": 0, "btm": 0, "top": 1, "both": 2}[line_split[2]]
            if len(line_split) == 3:
                fade_frames = None
            elif line_split[4] == "default":
                fade_frames = None
            else:
                try:
                    fade_frames = float(line_split[4])
                except ValueError:
                    raise TypeError(f"Fade: Time invalid (line {self.line_num})")
                if line_split[5] == "frames":
                    fade_frames = int(fade_frames)
                elif line_split[5] == "seconds":
                    fade_frames = int(fade_frames * 60.0)
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("fade", [fade_in, fade_screen, fade_frames])
            )
        elif line_split[0] == "load":
            if not match_syntax(line_split, ("load", ("bottom", "btm", "top"), None)):
                raise SyntaxError(f"Load does not match syntax (line {self.line_num})")
            load_screen = 0 if line_split[1] in ("bottom", "btm") else 1
            load_path = line_split[2]
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("bg_load", [load_path, load_screen])
            )
        elif line_split[0] == "set":
            if not match_syntax(line_split, ("set", ("room", "mode", "next_mode", "movie", "event", "puzzle"), None)):
                raise SyntaxError(f"Set does not match syntax (line {self.line_num})")
            set_value = line_split[2]
            if line_split[1] not in ("mode", "next_mode"):
                try:
                    set_value = int(set_value)
                except ValueError:
                    raise TypeError(f"Set: Value type invalid (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name(f"set_{line_split[1]}", [set_value])
            )
        elif line_split[0] == "show":
            if not match_syntax(line_split, ("show", None)):
                raise SyntaxError(f"Show does not match syntax (line {self.line_num})")
            char_name = line_split[1]
            if char_name not in self.defined_characters:
                raise ValueError(f"Show: Character {char_name} does not exist (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("chr_show", [self.defined_characters.index(char_name)])
            )
        elif line_split[0] == "hide":
            if not match_syntax(line_split, ("hide", None)):
                raise SyntaxError(f"Hide does not match syntax (line {self.line_num})")
            char_name = line_split[1]
            if char_name not in self.defined_characters:
                raise ValueError(f"Hide: Character {char_name} does not exist (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("chr_hide", [self.defined_characters.index(char_name)])
            )
        elif line_split[0] == "visible":
            if not match_syntax(line_split, ("visible", None)):
                raise SyntaxError(f"Visible does not match syntax (line {self.line_num})")
            char_name = line_split[1]
            if char_name not in self.defined_characters:
                raise ValueError(f"Visible: Character {char_name} does not exist (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("chr_visibility",
                                                      [self.defined_characters.index(char_name),
                                                       True])
            )
        elif line_split[0] == "invisible":
            if not match_syntax(line_split, ("invisible", None)):
                raise SyntaxError(f"Invisible does not match syntax (line {self.line_num})")
            char_name = line_split[1]
            if char_name not in self.defined_characters:
                raise ValueError(f"Invisible: Character {char_name} does not exist (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("chr_visibility", [self.defined_characters.index(char_name),
                                                                         False])
            )
        elif line_split[0] == "chapter":
            if not match_syntax(line_split, ("chapter", None)):
                raise SyntaxError(f"Chapter does not match syntax (line {self.line_num})")
            try:
                chapter_num = int(line_split[1])
            except ValueError:
                raise TypeError(f"Chapter: Invalid number type {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("show_chapter", [chapter_num])
            )
        elif line_split[0] in ("slot", "pos"):
            if not match_syntax(line_split, (("slot", "pos"), None, None)):
                raise SyntaxError(f"Slot does not match syntax (line {self.line_num})")
            char_name = line_split[1]
            if char_name not in self.defined_characters:
                raise ValueError(f"Slot: Character {char_name} does not exist (line {self.line_num})")
            try:
                slot_num = int(line_split[2])
            except ValueError:
                raise TypeError(f"Slot: Invalid number (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("chr_slot", [self.defined_characters.index(char_name), slot_num])
            )
        elif line_split[0] == "animation":
            if not match_syntax(line_split, ("animation", None, None)):
                raise SyntaxError(f"Animation does not match syntax (line {self.line_num})")
            char_name = line_split[1]
            char_id = self.ev.characters[self.defined_characters.index(char_name)]
            if char_name not in self.defined_characters:
                raise ValueError(f"Animation: Character {char_name} does not exist (line {self.line_num})")
            animation = line_split[2]
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("chr_anim", [char_id, animation])
            )
        elif line_split[0] == "wait":
            if not match_syntax(line_split, ("wait", None, ("frames", "seconds"))):
                raise SyntaxError(f"Wait does not match syntax (line {self.line_num})")
            try:
                wait_frames = float(line_split[1])
            except ValueError:
                raise TypeError(f"Fade: Time invalid (line {self.line_num})")
            if line_split[2] == "frames":
                wait_frames = int(wait_frames)
            elif line_split[2] == "seconds":
                wait_frames = int(wait_frames * 60.0)
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("wait", [wait_frames])
            )
        elif line_split[0] == "opacity":
            if not match_syntax(line_split, ("opacity", None), ((None,),)):
                raise SyntaxError(f"Opacity does not match syntax (line {self.line_num})")
            try:
                opacity = int(line_split[1])
            except ValueError:
                raise TypeError(f"Opacity: Invalid value (line {self.line_num})")
            optional = [15, 5, 0]
            if len(line_split) == 3:
                optional_str = split_quoted(line_split[2])
                if len(optional_str) != 3:
                    raise SyntaxError(f"Opacity: Optional arguments do not match syntax (line {self.line_num})")
                for i in range(3):
                    try:
                        optional[i] = int(optional_str[i])
                    except ValueError:
                        raise TypeError(f"Opacity: Invalid optional arguments (line {self.line_num})")
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("bg_opacity", optional + [opacity])
            )
        elif line_split[0] in self.defined_characters:
            line_split_dialogue = split_quoted(line, separator=":", remove_quotes=False)
            cmd = line_split_dialogue[0]
            lines = [":".join(line_split_dialogue[1:])[1:]]
            line_split = split_quoted(cmd)
            if not match_syntax(line_split, (None, None, None, None), (("voice", None),)):
                raise SyntaxError(f"Dialogue does not match syntax (line {self.line_num})")
            if len(line_split) > 4:
                try:
                    voice = int(line_split[5])
                except ValueError:
                    raise TypeError(f"Dialogue: Voice invalid value (line {self.line_num})")
                self.ev.gds.commands.append(
                    event_gds_parser.reverse_command_name("set_voice", [voice])
                )
            gds_number = self.text_gds_number
            self.text_gds_number += 100
            character_id = self.ev.characters[self.defined_characters.index(line_split[0])]
            start_animation = "NONE" if line_split[1] == "" else line_split[1]
            end_animation = "NONE" if line_split[2] == "" else line_split[2]
            try:
                sound_pitch = int(line_split[3])
            except ValueError:
                raise TypeError(f"Dialogue: Invalid sound pitch (line {self.line_num})")
            while self.peek_line().startswith("    "):
                lines.append(self.get_line()[4:])
            self.ev.gds.commands.append(
                event_gds_parser.reverse_command_name("dial", [gds_number, character_id, start_animation, end_animation,
                                                               sound_pitch, "\n".join(lines)])
            )
        elif line_split[0] == "bgm":
            if len(line_split) == 1:
                raise SyntaxError(f"Bgm invalid (line {self.line_num})")
            if line_split[1] == "fade":
                if not match_syntax(line_split, ("bgm", "fade", ("in", "out")), ((None,),)):
                    raise SyntaxError(f"Bgm fade does not match syntax (line {self.line_num})")
                args = [0.0, 2] if line_split[2] == "out" else [1.0, 253]
                if len(line_split) == 4:
                    args_str = split_quoted(line_split[3])
                    if not match_syntax(args_str, (None, None)):
                        raise SyntaxError(f"Bgm fade: Optional does not match syntax (line {self.line_num})")
                    try:
                        args[0] = float(args_str[0])
                        args[1] = int(args_str[1])
                    except ValueError:
                        raise TypeError(f"Bgm fade: Optional arguments invalid (line {self.line_num})")
                self.ev.gds.commands.append(event_gds_parser.reverse_command_name(f"bgm_fade_{line_split[2]}", args))
            elif line_split[1] == "play":
                if not match_syntax(line_split, ("bgm", "play", None, "at", "volume", None), ((None,),)):
                    raise SyntaxError(f"Bgm play does not match syntax (line {self.line_num})")
                try:
                    bgm_id = int(line_split[2])
                    volume = float(line_split[5])
                    unk = 0
                    if len(line_split) == 7:
                        unk = int(line_split[6])
                except ValueError:
                    raise TypeError(f"Bgm play: Invalid arguments (line {self.line_num})")
                self.ev.gds.commands.append(event_gds_parser.reverse_command_name("bg_music", [bgm_id, volume, unk]))
            else:
                raise SyntaxError(f"Unknown bgm command (line {self.line_num})")
        elif line_split[0] == "tap":
            if not match_syntax(line_split, ("tap",)):
                raise SyntaxError(f"Tap does not match syntax (line {self.line_num})")
            self.ev.gds.commands.append(event_gds_parser.reverse_command_name("wait_tap", []))
        elif line_split[0] == "shake":
            if not match_syntax(line_split, ("shake",), ((None,),)):
                raise SyntaxError(f"Shake does not match syntax (line {self.line_num})")
            default = 30
            if len(line_split) == 2:
                try:
                    default = int(line_split[2])
                except ValueError:
                    raise TypeError(f"Shake: Invalid value (line {self.line_num})")
            self.ev.gds.commands.append(event_gds_parser.reverse_command_name("bg_shake", [default]))
        elif line_split[0] == "sfx":
            if not match_syntax(line_split, ("sfx", ("sad", "sed"), None)):
                raise SyntaxError(f"Sfx does not match syntax (line {self.line_num})")
            try:
                sfx_id = int(line_split[2])
            except ValueError:
                raise TypeError(f"Sfx: Invalid sfx id (line {self.line_num})")
            self.ev.gds.commands.append(event_gds_parser.reverse_command_name(f"sfx_{line_split[1]}", [sfx_id]))
        elif line_split[0] == "dialogue":
            if not match_syntax(line_split, ("dialogue", "sfx", None), ((None,),)):
                raise SyntaxError(f"Dialogue sfx does not match syntax (line {self.line_num})")
            try:
                sfx_id = int(line_split[2])
                default = [1.0, 0.0, 1]
                if len(line_split) == 4:
                    default_str = split_quoted(line_split[3])
                    default[0] = float(default_str[0])
                    default[1] = float(default_str[1])
                    default[2] = int(default_str[2])
            except ValueError:
                raise TypeError(f"Dialogue sfx: Invalid values (line {self.line_num})")
            self.ev.gds.commands.append(event_gds_parser.reverse_command_name("dialogue_sfx", [sfx_id] + default))
        elif re.match("^0x[0-9a-fA-F]{2}$", line_split[0]):
            args = line_split[1:]
            parsed = []
            for arg in args:
                parsed.append(DCCParser.convert_variable(arg, strings_unquoted=True))
            self.ev.gds.commands.append(event_gds_parser.reverse_command_name(f"gds_{line_split[0]}", parsed))
        else:
            raise SyntaxError(f"Unknown command (line {self.line_num})")


if __name__ == '__main__':
    with open("../../e10_030.txt", "rb") as f:
        p = EventScriptParser(f.read().decode("utf-8").replace("\r\n", "\n"))
        try:
            p.parse()
        except Exception as e:
            print(p.ev.gds.commands)
            raise e
        print(p.ev.gds.commands)
