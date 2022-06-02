import formats.gds
import typing
if typing.TYPE_CHECKING:
    from formats import event
import utility.replace_substitutions as subs
from formats.parsers.dcc import DCCParser


class GDSParser:
    def __init__(self):
        self.command_name_table = {}

    def parse_cmd(self, code: str, is_code=True):
        for v in self.command_name_table.values():
            if len(v) == 3:
                code_, not_code, _ = v
            else:
                code_, not_code = v
            if is_code:
                if code == code_:
                    return not_code
            else:
                if code == not_code:
                    return code_
        return code

    def parse_command_name(self, command: formats.gds.GDSCommand, is_code=True):
        param_names = [f"unk{i}" for i in range(len(command.params))]
        if command.command not in self.command_name_table.keys():
            return f"gds_{hex(command.command)}", command.params, param_names
        if len(self.command_name_table[command.command]) == 3:
            param_names = self.command_name_table[command.command][2]
        return self.command_name_table[command.command][0 if is_code else 1], command.params.copy(), param_names

    def reverse_command_name(self, command: str, params, is_code=True):
        if command.startswith("gds_"):
            return formats.gds.GDSCommand(int(command[4:], 16), params.copy())
        for key in self.command_name_table.keys():
            if self.command_name_table[key][0 if is_code else 1] == command:
                return formats.gds.GDSCommand(key, params.copy())
        raise ValueError(f"{command} is not a valid command")

    def parse_into_dcc(self, gds: formats.gds.GDS, dcc_parser: DCCParser):
        dcc_parser.get_path("script", create=True)
        for param in gds.params:
            dcc_parser["script::unnamed"].append(param)
        for cmd in gds.commands:
            cmd_text, params, _ = self.parse_command_name(cmd)
            dcc_parser["script::calls"].append({
                "func": cmd_text,
                "parameters": params.copy()
            })

    def parse_from_dcc(self, gds: formats.gds.GDS, dcc_parser: DCCParser):
        if not dcc_parser.exists("script"):
            return False, "Missing script"

        gds.commands = []
        gds.params = []
        for param in dcc_parser["script::unnamed"]:
            gds.params.append(param)
        for call in dcc_parser["script::calls"]:
            func = call["func"]
            params = call["parameters"]
            command = self.reverse_command_name(func, params)
            gds.commands.append(command)
        return True, ""

class InputGDSParser(GDSParser):
    def __init__(self):
        super(InputGDSParser, self).__init__()
        self.command_name_table = {
            0x43: ["load_input_bg", "Load Input Background"],
            0x42: ["set_answer", "Set Answer"],
            0x41: ["set_input_type", "Set Input Type"]
        }


class MultipleChoiceGDSParser(GDSParser):
    def __init__(self):
        super(MultipleChoiceGDSParser, self).__init__()
        self.command_name_table = {
            0x14: ["add_button", "Add Button"]
        }


class TileRotate2GDSParser(GDSParser):
    def __init__(self):
        super(TileRotate2GDSParser, self).__init__()
        self.command_name_table = {
            0x60: ["start_positions_maybe", "Set Start Positions"],
            0x55: ["create_slot", "Create Slot"],
            # parameters: (x: int, y: int) of top left corner
            0x54: ["set_tile_image", "Set Tile Image"],
            # parameters: (name: str) of the file at data_lt2/ani/nazo/tile/<> (ends in .spr)
            0x57: ["create_tile", "Create Tile"],
            # parameters: (unk0: int, unk1: int, unk2: int, anim1: str, anim2: str, anim3: str,
            #              slot: int) creates a tile with the specified anim at the specified slot
            0x59: ["set_tile_size", "Set Tile Size"],
            # parameters: (x_maybe: int, y_maybe: int, w: int, h: int) always after a 0x57
            0x5a: ["set_tile_solution", "Set Tile Solution"],
            # parameters: (tile: int, solution: int)
        }


class EventGDSParser(GDSParser):
    def __init__(self, ev: 'event.Event' = None):
        super(EventGDSParser, self).__init__()
        self.ev: 'event.Event' = ev
        fade = ["fade", "Fade", ["Fade In", "Fade Screen", "Fade Frames"]]
        bg_load = ["bg_load", "Load Background", ["Path", "Screen"]]
        self.command_name_table = {
            0x2: fade,
            0x3: fade,
            0x4: ["dial", "Dialogue", ["Text GDS Number", "Character ID", "Start Animation",
                                       "End Animation", "Sound Pitch?", "Text"]],
            0x5: ["set_room", "Set Room", ["Room ID"]],
            0x6: ["set_mode", "Set Mode", ["Mode"]],
            0x7: ["set_next_mode", "Set Next Mode", ["Mode"]],
            0x8: ["set_movie", "Set Movie", ["Movie ID"]],
            0x9: ["set_event", "Set Event", ["Event ID"]],
            0xb: ["set_puzzle", "Set Puzzle", ["Puzzle ID"]],
            0x21: bg_load,
            0x22: bg_load,
            0x2a: ["chr_show", "Show Character", ["Character Index"]],
            0x2b: ["chr_hide", "Hide Character", ["Character Index"]],
            0x2c: ["chr_visibility", "Set Character Visibility", ["Character Index", "Visibility"]],
            0x2d: ["show_chapter", "Show Chapter", ["Chapter Number"]],
            0x30: ["chr_slot", "Set Character Slot", ["Character Index", "Slot"]],
            0x31: ["wait", "Wait", ["Wait Frames"]],
            0x32: fade,
            0x33: fade,
            0x37: ["bg_opacity", "Set Background Opacity"],
            0x3f: ["chr_anim", "Set Character Animation", ["Character ID", "Animation"]],
            0x5c: ["set_voice", "Set Voice", ["Voice ID"]],
            0x5d: ["sfx_sad", "Play SAD SFX", ["SFX ID"]],
            0x5e: ["sfx_sed", "Play SED SFX", ["SFX ID"]],
            0x62: ["bg_music", "Play Background Music", ["Music ID", "Volume", "unk2"]],
            0x69: ["wait_tap", "Wait Tap"],
            0x6a: ["bg_shake", "Shake Background"],
            0x72: fade,
            0x80: fade,
            0x87: fade,
            0x88: fade,
            0x8a: ["bgm_fade_out", "Fade Out BG Music"],
            0x8b: ["bgm_fade_in", "Fade In BG Music"],
            0x99: ["dialogue_sfx", "Set Dialogue SFX"],
        }

    def parse_command_name(self, command: formats.gds.GDSCommand, is_code=True):
        func, params, param_names = super(EventGDSParser, self).parse_command_name(command, is_code=is_code)
        if command.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x80, 0x87, 0x88]:  # fade
            params_1 = [False, 0, None]
            params_1[0] = command.command in [0x2, 0x32, 0x80, 0x88]
            if command.command in [0x2, 0x3, 0x72, 0x80]:
                params_1[1] = 2  # both screens
            elif command.command in [0x32, 0x33]:
                params_1[1] = 0  # btm screen
            elif command.command in [0x87, 0x88]:
                params_1[1] = 1  # top screen
            if command.command in [0x72, 0x80, 0x87, 0x88]:
                params_1[2] = params[0]  # timed
            params = params_1
        elif command.command in [0x21, 0x22]:  # BG Load
            params = [params[0], 0]
            params[-1] = 0 if command.command == 0x21 else 1
        elif command.command == 0x2c:
            params[1] = True if params[1] > 0 else False
        elif command.command == 0x4:
            params = [params[0] if params else 0]
            if self.ev is not None and params:
                dial_gds = self.ev.get_text(params[0])
                if len(dial_gds.params) == 0:
                    params.extend([0, "NONE", "NONE", 2, ""])
                else:
                    params.extend(dial_gds.params[:4])
                    params.append(subs.replace_substitutions(dial_gds.params[4]))
            else:
                params.extend([0, "NONE", "NONE", 2, ""])
        elif command.command == 0x37:
            param_names[3] = "Opacity"
        elif command.command == 0x99:
            param_names[0] = "SAD SFX ID"
        return func, params, param_names

    def reverse_command_name(self, command: str, params, is_code=True):
        gds_cmd = super(EventGDSParser, self).reverse_command_name(command, params, is_code=is_code)
        command = self.parse_cmd(command, is_code=False)
        if command == "fade":  # fade
            gds_cmd.params = []
            if params[0] is True:  # [0x2, 0x32, 0x80, 0x88]
                if params[1] == 2:  # [0x2, 0x80]
                    if params[2] is None or params[2] == -1:  # [0x2]
                        gds_cmd.command = 0x2
                    else:  # [0x80]
                        gds_cmd.command = 0x80
                elif params[1] == 0:  # [0x32]
                    gds_cmd.command = 0x32
                elif params[1] == 1:  # [0x88]
                    gds_cmd.command = 0x88
                    if params[2] is None or params[2] == -1:
                        params[2] = 42
            else:  # [0x3, 0x33, 0x72, 0x87]
                if params[1] == 2:  # [0x3, 0x72]
                    if params[2] is None or params[2] == -1:  # [0x3]
                        gds_cmd.command = 0x3
                    else:  # [0x72]
                        gds_cmd.command = 0x72
                elif params[1] == 0:  # [0x33]
                    gds_cmd.command = 0x33
                elif params[1] == 1:  # [0x87]
                    gds_cmd.command = 0x87
                    if params[2] is None or params[2] == -1:
                        params[2] = 42
            if gds_cmd.command in [0x72, 0x80, 0x87, 0x88]:
                gds_cmd.params = params[2:]
        elif command == "bg_load":
            gds_cmd.command = 0x21 if params[-1] == 0 else 0x22
            gds_cmd.params = [params[0], 3]
        elif command == "chr_visibility":
            gds_cmd.params[1] = 2.0 if params[1] else -2.0
        elif command == "dial":
            gds_cmd.params = [params[0]]

            dial_gds = formats.gds.GDS()
            dial_gds.params = params[1:]
            dial_gds.params[4] = subs.convert_substitutions(dial_gds.params[4])

            if self.ev is not None:
                self.ev.texts[params[0]] = dial_gds
        return gds_cmd
