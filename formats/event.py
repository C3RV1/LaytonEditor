# Ported from shortbrim
import formats.binary as binary
import formats.gds
import formats.filesystem as fs
import formats.dcc_parser as dcc
import utility.replace_substitutions as subs
from typing import Optional

from formats import conf


class Event:
    def __init__(self, rom: fs.NintendoDSRom = None):
        self.rom = rom
        self.event_id = 0

        self.event_gds: formats.gds.GDS = formats.gds.GDS()
        self.event_texts: Optional[fs.PlzArchive] = None

        self.map_top_id = 0
        self.map_bottom_id = 0
        self.characters = [0, 0, 0, 0, 0, 0, 0, 0]
        self.characters_pos = [0, 0, 0, 0, 0, 0, 0, 0]
        self.characters_shown = [False, False, False, False, False, False, False, False]
        self.characters_anim_index = [0, 0, 0, 0, 0, 0, 0, 0]

        self.original = b""

    def set_event_id(self, new_id):
        self.event_id = new_id

    def resolve_event_id(self):
        prefix = self.event_id // 1000
        postfix = self.event_id % 1000
        complete = str(prefix)
        if prefix == 24:
            if postfix < 300:
                complete += "a"
            elif postfix < 600:
                complete += "b"
            else:
                complete += "c"
        return str(prefix), str(postfix).zfill(3), complete

    def load_from_rom(self):
        if self.rom is None:
            return
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        file_id = events_packed.filenames.index(f"d{prefix}_{postfix}.dat")
        self.load(events_packed.files[file_id])
        self.load_gds()
        self.load_texts()

    def save_to_rom(self):
        if self.rom is None:
            return
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        file = events_packed.open(f"d{prefix}_{postfix}.dat", "wb+")
        self.write(binary.BinaryWriter(file))
        file.close()
        self.save_gds()

    def load(self, data: bytes):
        self.original = data

        reader = binary.BinaryReader(data)
        self.map_bottom_id = reader.read_uint16()
        self.map_top_id = reader.read_uint16()

        reader.c += 2

        self.characters = []
        for _indexChar in range(8):
            self.characters.append(reader.read_uint8())
        self.characters_pos = []
        for _indexChar in range(8):
            self.characters_pos.append(reader.read_uint8())
        self.characters_shown = []
        for _indexChar in range(8):
            if reader.read_uint8() == 0:
                self.characters_shown.append(False)
            else:
                self.characters_shown.append(True)
        self.characters_anim_index = []
        for _indexChar in range(8):
            self.characters_anim_index.append(reader.read_uint8())

    def write(self, wtr):
        if not isinstance(wtr, binary.BinaryWriter):
            wtr = binary.BinaryWriter()
        wtr.write_uint16(self.map_bottom_id)
        wtr.write_uint16(self.map_top_id)
        wtr.c += 2

        for char in self.characters:
            wtr.write_uint8(char)
        for char_pos in self.characters_pos:
            wtr.write_uint8(char_pos)
        for char_show in self.characters_shown:
            wtr.write_uint8(1 if char_show else 0)
        for char_anim in self.characters_anim_index:
            wtr.write_uint8(char_anim)

        wtr.write(self.original[-2:])

        return wtr.data

    def load_gds(self):
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        self.event_gds = formats.gds.GDS(f"e{prefix}_{postfix}.gds", rom=events_packed)

    def save_gds(self):
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        gds_file = events_packed.open(f"e{prefix}_{postfix}.gds", "wb+")
        self.event_gds.write_stream(gds_file)
        gds_file.close()

    def load_texts(self):
        prefix, postfix, complete = self.resolve_event_id()
        self.event_texts = self.rom.get_archive(f"data_lt2/event/?/ev_t{complete}.plz".replace("?", conf.LANG))

    def get_text(self, text_num):
        prefix, postfix, complete = self.resolve_event_id()
        if f"t{prefix}_{postfix}_{text_num}.gds" not in self.event_texts.filenames:
            return formats.gds.GDS()
        return formats.gds.GDS(f"t{prefix}_{postfix}_{text_num}.gds", rom=self.event_texts)

    def to_readable(self):
        parser = dcc.Parser()
        parser.reset()
        parser.get_path("evdat", create=True)
        parser.set_named("evdat.map_top_id", self.map_top_id)
        parser.set_named("evdat.map_btm_id", self.map_bottom_id)
        for i in range(len(self.characters)):
            parser.get_path(f"evdat.char{i}", create=True)
            parser.set_named(f"evdat.char{i}.char", self.characters[i])
            parser.set_named(f"evdat.char{i}.pos", self.characters_pos[i])
            parser.set_named(f"evdat.char{i}.shown", self.characters_shown[i])
            parser.set_named(f"evdat.char{i}.anim", self.characters_anim_index[i])

        parser.get_path("evs", create=True)
        for cmd in self.event_gds.commands:
            func, params, _param_names = self.convert_command(cmd, for_code=True)
            parser["evs::calls"].append({
                "func": func,
                "parameters": params
            })

        return parser.serialize()

    def convert_command(self, cmd: formats.gds.GDSCommand, for_code=True):
        func = f"gds_{hex(cmd.command)}"
        name = func
        params = cmd.params.copy()
        param_names = [f"unk{i}" for i in range(len(params))]
        if cmd.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x80, 0x87, 0x88]:  # fade command
            func = "fade"
            name = "Fade"
            param_names = ["Fade In", "Fade Screen", "Fade Frames"]
            params_1 = [False, 0, None]  # fade_in, fade_screen, fade_time
            params_1[0] = cmd.command in [0x2, 0x32, 0x80, 0x88]
            if cmd.command in [0x2, 0x3, 0x72, 0x80]:
                params_1[1] = 2  # both screens
            elif cmd.command in [0x32, 0x33]:
                params_1[1] = 0  # btm screen
            elif cmd.command in [0x87, 0x88]:
                params_1[1] = 1  # top screen
            if cmd.command in [0x72, 0x80, 0x87, 0x88]:
                params_1[2] = params[0]  # timed
            params = params_1
        elif cmd.command in [0x21, 0x22]:
            func = "bg_load"
            name = "Load Background"
            param_names = ["Path", "Screen"]
            params = [params[0], 0]
            params[-1] = 0 if cmd.command == 0x21 else 1  # screen for which to change the bg
        elif cmd.command == 0x5:
            func = "set_room"
            name = "Set Room"
            param_names = ["Room ID"]
        elif cmd.command == 0x6:
            func = "set_mode"
            name = "Set Mode"
            param_names = ["Mode"]
        elif cmd.command == 0x7:
            func = "set_next_mode"
            name = "Set Next Mode"
            param_names = ["Mode"]
        elif cmd.command == 0x8:
            func = "set_movie"
            name = "Set Movie"
            param_names = ["Movie ID"]
        elif cmd.command == 0x9:
            func = "set_event"
            name = "Set Event"
            param_names = ["Event ID"]
        elif cmd.command == 0xb:
            func = "set_puzzle"
            name = "Set Puzzle"
            param_names = ["Puzzle ID"]
        elif cmd.command == 0x2a:
            func = "chr_show"
            name = "Show Character"
            param_names = ["Character Index"]
        elif cmd.command == 0x2b:
            func = "chr_hide"
            name = "Hide Character"
            param_names = ["Character Index"]
        elif cmd.command == 0x2c:
            func = "chr_visibility"
            name = "Set Character Visibility"
            param_names = ["Character Index", "show"]
            params[1] = True if params[1] > 0 else False
        elif cmd.command == 0x2d:
            func = "show_chapter"
            name = "Show Chapter"
            param_names = ["chapter_num"]
        elif cmd.command == 0x30:
            func = "chr_slot"
            name = "Set Character Slot"
            param_names = ["Character Index", "Slot"]
        elif cmd.command == 0x31:
            func = "wait"
            name = "Wait"
            param_names = ["Wait Frames"]
        elif cmd.command == 0x37:
            func = "bg_opacity"
            name = "Background Opacity"
            param_names[3] = "Opacity"
        elif cmd.command == 0x3f:
            func = "chr_anim"
            name = "Set Character Animation"
            param_names = ["Character ID", "Anim"]
        elif cmd.command == 0x5c:
            func = "set_voice"
            name = "Set Voice"
            param_names = ["Voice ID"]
        elif cmd.command == 0x5d:
            func = "sfx_sad"
            name = "Play SAD SFX"
            param_names = ["SFX ID"]
        elif cmd.command == 0x5e:
            func = "sfx_sed"
            name = "Play SED SFX"
            param_names = ["SFX ID"]
        elif cmd.command == 0x62:
            func = "bg_music"
            name = "Play Background Music"
            param_names = ["Music ID", "Volume", "unk2"]
        elif cmd.command == 0x6a:
            func = "bg_shake"
            name = "Shake Background"
            param_names = []
        elif cmd.command == 0x8a:
            func = "bgm_fade_out"
            name = "Fade Out BG Music"
        elif cmd.command == 0x8b:
            func = "bgm_fade_in"
            name = "Fade In BG Music"
        elif cmd.command == 0x99:
            func = "dialogue_sfx"
            name = "Set Dialogue SFX"
            param_names[0] = "SAD SFX ID"
        elif cmd.command == 0x4:
            func = "dialogue"
            name = "Dialogue"
            param_names = ["Text Gds Number", "Character ID", "Start Animation",
                           "End Animation", "unk4", "Text"]
            dial_gds = self.get_text(params[0])
            params = [params[0]]
            params.extend(dial_gds.params[:4])
            params.append(subs.replace_substitutions(dial_gds.params[4]))
        if not for_code:
            func = name
        return func, params, param_names

    def from_readable(self, readable):
        parser = dcc.Parser()
        try:
            parser.parse(readable)
        except Exception as e:
            return False, str(e)

        required_paths = ["evdat.map_top_id", "evdat.map_btm_id", "evs"]
        for i in range(8):
            required_paths.extend([f"evdat.char{i}.char", f"evdat.char{i}.pos", f"evdat.char{i}.shown",
                                   f"evdat.char{i}.anim"])

        for req_path in required_paths:
            if not parser.exists(req_path):
                return False, f"Missing {req_path}"

        self.map_top_id = parser["evdat.map_top_id"]
        self.map_bottom_id = parser["evdat.map_btm_id"]

        for i in range(8):
            self.characters[i] = parser[f"evdat.char{i}.char"]
            self.characters_pos[i] = parser[f"evdat.char{i}.pos"]
            self.characters_shown[i] = parser[f"evdat.char{i}.shown"]
            self.characters_anim_index[i] = parser[f"evdat.char{i}.anim"]

        dial_files = self.event_texts.filenames
        prefix, postfix, complete = self.resolve_event_id()
        for filename in dial_files:
            if filename.startswith(f"e{prefix}_{postfix}"):
                self.event_texts.remove_file(filename)

        self.event_gds.commands = []
        for call in parser["evs::calls"]:
            func = call["func"]
            params = call["parameters"]
            command = self.revert_command(func, params)
            self.event_gds.commands.append(command)
        return True, ""

    def revert_command(self, func, params):
        command = formats.gds.GDSCommand(0)
        params = params.copy()
        if func == "fade" or func == "Fade":
            if params[0] is True:  # [0x2, 0x32, 0x80, 0x88]
                if params[1] == 2:  # [0x2, 0x80]
                    if params[2] is None or params[2] == -1:  # [0x2]
                        command.command = 0x2
                    else:  # [0x80]
                        command.command = 0x80
                elif params[1] == 0:  # [0x32]
                    command.command = 0x32
                elif params[1] == 1:  # [0x88]
                    command.command = 0x88
                    if params[2] is None or params[2] == -1:
                        params[2] = 42
            else:  # [0x3, 0x33, 0x72, 0x87]
                if params[1] == 2:  # [0x3, 0x72]
                    if params[2] is None or params[2] == -1:  # [0x3]
                        command.command = 0x3
                    else:  # [0x72]
                        command.command = 0x72
                elif params[1] == 0:  # [0x33]
                    command.command = 0x33
                elif params[1] == 1:  # [0x87]
                    command.command = 0x87
                    if params[2] is None or params[2] == -1:
                        params[2] = 42
            if command.command in [0x72, 0x80, 0x87, 0x88]:
                command.params = params[2:]
        elif func == "set_room" or func == "Set Room":
            command.command = 0x5
            command.params = params
        elif func == "set_mode" or func == "Set Mode":
            command.command = 0x6
            command.params = params
        elif func == "set_next_mode" or func == "Set Next Mode":
            command.command = 0x7
            command.params = params
        elif func == "set_movie" or func == "Set Movie":
            command.command = 0x8
            command.params = params
        elif func == "set_event" or func == "Set Event":
            command.command = 0x9
            command.params = params
        elif func == "set_puzzle" or func == "Set Puzzle":
            command.command = 0xb
            command.params = params
        elif func == "bg_load" or func == "Load Background":
            command.command = 0x21 if params[-1] == 0 else 0x22
            command.params = [params[0], 3]
        elif func == "chr_show" or func == "Show Character":
            command.command = 0x2a
            command.params = params
        elif func == "chr_hide" or func == "Hide Character":
            command.command = 0x2b
            command.params = params
        elif func == "chr_visibility" or func == "Set Character Visibility":
            command.command = 0x2c
            params[1] = 2.0 if params[1] else -2.0
            command.params = params
        elif func == "show_chapter" or func == "Show Chapter":
            command.command = 0x2d
            command.params = params
        elif func == "chr_slot" or func == "Set Character Slot":
            command.command = 0x30
            command.params = params
        elif func == "wait" or func == "Wait":
            command.command = 0x31
            command.params = params
        elif func == "bg_opacity" or func == "Set Background Opacity":
            command.command = 0x37
            command.params = params
        elif func == "chr_anim" or func == "Set Character Animation":
            command.command = 0x3f
            command.params = params
        elif func == "set_voice" or func == "Set Voice":
            command.command = 0x5c
            command.params = params
        elif func == "sfx_sad" or func == "Play SAD SFX":
            command.command = 0x5d
            command.params = params
        elif func == "sfx_sed" or func == "Play SED SFX":
            command.command = 0x5e
            command.params = params
        elif func == "bg_music" or func == "Play Background Music":
            command.command = 0x62
            command.params = params
        elif func == "bg_shake" or func == "Shake Background":
            command.command = 0x6a
            command.params = params
        elif func == "bgm_fade_out" or func == "Fade Out BG Music":
            command.command = 0x8a
            command.params = params
        elif func == "bgm_fade_in" or func == "Fade In BG Music":
            command.command = 0x8b
            command.params = params
        elif func == "dialogue_sfx" or func == "Set Dialogue SFX":
            command.command = 0x99
            command.params = params
        elif func == "dialogue" or func == "Dialogue":
            command.command = 0x4
            command.params = [params[0]]

            dial_gds = formats.gds.GDS()
            dial_gds.params = params[1:]
            dial_gds.params[4] = subs.convert_substitutions(dial_gds.params[4])

            prefix, postfix, complete = self.resolve_event_id()
            dial_gds_file = self.event_texts.open(f"t{prefix}_{postfix}_{params[0]}.gds", "wb+")
            dial_gds.write_stream(dial_gds_file)
            dial_gds_file.close()
        elif func.startswith("gds_"):
            command.command = int(func[4:], 16)
            command.params = params
        else:
            return False, f"Function {repr(func)} not found"
        return command
