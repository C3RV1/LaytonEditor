# Ported from shortbrim
import formats.binary as binary
import formats.gds
import formats.filesystem as fs
import formats.dcc_parser as dcc
import utility.replace_substitutions as subs
from typing import Optional


class EventData:
    def __init__(self, rom: fs.NintendoDSRom = None, lang="en"):
        self.rom = rom
        self.event_id = 0

        self.event_gds: Optional[formats.gds.GDS] = formats.gds.GDS()
        self.event_texts: Optional[fs.PlzArchive] = None

        self.map_top_id = 0
        self.map_bottom_id = 0
        self.characters = [0, 0, 0, 0, 0, 0, 0, 0]
        self.characters_pos = [0, 0, 0, 0, 0, 0, 0, 0]
        self.characters_shown = [False, False, False, False, False, False, False, False]
        self.characters_anim_index = [0, 0, 0, 0, 0, 0, 0, 0]
        self.lang = lang

        self.original = ""

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
        self.event_texts = self.rom.get_archive(f"data_lt2/event/?/ev_t{complete}.plz".replace("?", self.lang))

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
        parser.get_path(f"evdat.characters", create=True)
        for i in range(len(self.characters)):
            parser.get_path(f"evdat.char{i}", create=True)
            parser.set_named(f"evdat.char{i}.char", self.characters[i])
            parser.set_named(f"evdat.char{i}.pos", self.characters_pos[i])
            parser.set_named(f"evdat.char{i}.shown", self.characters_shown[i])
            parser.set_named(f"evdat.char{i}.anim", self.characters_anim_index[i])

        parser.get_path("evs", create=True)
        for cmd in self.event_gds.commands:
            func = f"gds_{hex(cmd.command)}"
            params = cmd.params
            if cmd.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x80, 0x87, 0x88]:  # fade command
                func = "fade"
                params_1 = [False, 0, None]  # fade_in, fade_screen
                params_1[0] = cmd.command in [0x2, 0x32, 0x80, 0x88]
                if cmd.command in [0x2, 0x3, 0x72, 0x80]:
                    params_1[1] = 2  # both screens
                elif cmd.command in [0x32, 0x33]:
                    params_1[1] = 0  # btm screen
                elif cmd.command in [0x87, 0x88]:
                    params_1[1] = 1  # top screen
                if cmd.params in [0x72, 0x80, 0x87, 0x88]:
                    params_1[2] = params[0]  # timed
                params = params_1
            elif cmd.command in [0x21, 0x22]:
                func = "bg_load"
                params = [params[0], 0]
                params[1] = 0 if cmd.command == 0x21 else 1  # screen for which to change the bg
            elif cmd.command == 0x2a:
                func = "chr_show"
            elif cmd.command == 0x2b:
                func = "chr_hide"
            elif cmd.command == 0x2c:
                func = "chr_visibility"
            elif cmd.command == 0x30:
                func = "chr_slot"
            elif cmd.command == 0x31:
                func = "wait"
            elif cmd.command == 0x37:
                func = "bg_opacity?"
            elif cmd.command == 0x3f:
                func = "chr_anim"
            elif cmd.command == 0x5c:
                func = "set_voice"
            elif cmd.command == 0x5d:
                func = "sfx_sad"
            elif cmd.command == 0x6a:
                func = "bg_shake"
            elif cmd.command == 0x4:
                func = "dial"
                dial_gds = self.get_text(params[0])
                params = [params[0]]
                params.extend(dial_gds.params[:4])
                params.append(subs.replace_substitutions(dial_gds.params[4]))
            parser["evs::calls"].append({
                "func": func,
                "parameters": params
            })

        return parser.serialize()

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

        self.event_gds.commands = []
        for call in parser["evs::calls"]:
            func = call["func"]
            params = call["parameters"]
            print(func, params)
            command = formats.gds.GDSCommand(0)
            if func == "fade":
                if params[0] is True:  # [0x2, 0x32, 0x80, 0x88]
                    if params[1] == 2:  # [0x2, 0x80]
                        if params[2] is None:  # [0x2]
                            command.command = 0x2
                        else:  # [0x80]
                            command.command = 0x80
                    elif params[1] == 1:  # [0x32]
                        command.command = 0x32
                    elif params[1] == 0:  # [0x88]
                        command.command = 0x88
                else:  # [0x3, 0x33, 0x72, 0x87]
                    if params[1] == 2:  # [0x3, 0x72]
                        if params[2] is None:  # [0x3]
                            command.command = 0x3
                        else:  # [0x72]
                            command.command = 0x72
                    elif params[1] == 1:  # [0x33]
                        command.command = 0x33
                    elif params[1] == 0:  # [0x87]
                        command.command = 0x87
                if command.command in [0x72, 0x80, 0x87, 0x88]:
                    command.params = params[:1]
            elif func == "bg_load":
                command.command = 0x21 if params[1] == 0 else 0x22
                command.params = params[:1]
            elif func == "chr_show":
                command.command = 0x2a
                command.params = params
            elif func == "chr_hide":
                command.command = 0x2b
                command.params = params
            elif func == "chr_visibility":
                command.command = 0x2c
                command.params = params
            elif func == "chr_slot":
                command.command = 0x30
                command.params = params
            elif func == "wait":
                command.command = 0x31
                command.params = params
            elif func == "bg_opacity?":
                command.command = 0x37
                command.params = params
            elif func == "chr_anim":
                command.command = 0x3f
                command.params = params
            elif func == "set_voice":
                command.command = 0x5c
                command.params = params
            elif func == "sfx_sad":
                command.command = 0x5d
                command.params = params
            elif func == "bg_shake":
                command.command = 0x6a
                command.params = params
            elif func == "dial":
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
                return False, f"Function {func} not found"
            self.event_gds.commands.append(command)

        return True, ""
