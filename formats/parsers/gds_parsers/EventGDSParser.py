import formats.gds
from ..gds_parser import GDSParser
import typing
if typing.TYPE_CHECKING:
    from formats import event
import utility.replace_substitutions as subs


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
            0x6a: ["bg_shake", "Shake Background", ["unk0", "Screen"]],
            0x6b: ["bg_shake", "Shake Background", ["unk0", "Screen"]],
            0x71: ["reveal_chapter", "Reveal Mystery", ["Mystery ID"]],
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
        elif command.command in [0x6a, 0x6b]:
            params = [params[0], 0 if command.command == 0x6a else 1]
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
        elif command == "bg_shake":
            gds_cmd.command = 0x6a if params[1] == 0 else 0x6b
            gds_cmd.params = params[:1]
        elif command == "dial":
            gds_cmd.params = [params[0]]

            dial_gds = formats.gds.GDS()
            dial_gds.params = params[1:]
            dial_gds.params[4] = subs.convert_substitutions(dial_gds.params[4])

            if self.ev is not None:
                self.ev.texts[params[0]] = dial_gds
        return gds_cmd
