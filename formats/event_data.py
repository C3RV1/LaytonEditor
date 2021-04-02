# Ported from shortbrim
import formats.binary as bin
import formats.gds
import formats.filesystem as fs


class EventData:
    def __init__(self, rom: fs.NintendoDSRom = None, lang="en"):
        self.rom = rom
        self.event_id = 0

        self.event_gds: formats.gds.GDS = None
        self.event_texts: fs.PlzArchive = None

        self.map_top_id = 0
        self.map_bottom_id = 0
        self.characters = []
        self.characters_pos = []
        self.characters_shown = []
        self.characters_anim_index = []
        self.lang = lang

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

    def load(self, data: bytes):
        reader = bin.BinaryReader(data)
        self.map_bottom_id = reader.read_uint16()
        self.map_top_id = reader.read_uint16()

        reader.c += 2

        self.characters = []
        for _indexChar in range(8):
            temp_char = reader.read_uint8()
            self.characters.append(temp_char)
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

    def load_gds(self):
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        self.event_gds = formats.gds.GDS(f"e{prefix}_{postfix}.gds", rom=events_packed)

    def load_texts(self):
        prefix, postfix, complete = self.resolve_event_id()
        self.event_texts = self.rom.get_archive(f"data_lt2/event/?/ev_t{complete}.plz".replace("?", self.lang))

    def get_text(self, text_num):
        prefix, postfix, complete = self.resolve_event_id()
        return formats.gds.GDS(f"t{prefix}_{postfix}_{text_num}.gds", rom=self.event_texts)
