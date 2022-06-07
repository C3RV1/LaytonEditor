# Ported from shortbrim
import re

import formats.binary as binary
import formats.gds
import formats.filesystem as fs
import formats.parsers.dcc as dcc
from formats.parsers.gds_parsers import EventGDSParser
import formats.parsers.event_script as event_script
from typing import Optional

from formats import conf


class Event:
    def __init__(self, rom: fs.NintendoDSRom = None):
        self.rom = rom
        self.event_id = 0

        self.gds: formats.gds.GDS = formats.gds.GDS()
        self.texts_archive: Optional[fs.PlzArchive] = None
        self.texts = {}

        self.map_top_id = 0
        self.map_bottom_id = 0
        self.unk0 = 0
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
        self.clear_event_texts()
        self.save_texts()

    def load(self, data: bytes):
        self.original = data

        reader = binary.BinaryReader(data)
        self.map_bottom_id = reader.read_uint16()
        self.map_top_id = reader.read_uint16()
        self.unk0 = reader.read_uint16()

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
        wtr.write_uint16(self.unk0)

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
        if self.rom is None:
            return
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        self.gds = formats.gds.GDS(f"e{prefix}_{postfix}.gds", rom=events_packed)

    def save_gds(self):
        if self.rom is None:
            return
        prefix, postfix, complete = self.resolve_event_id()
        events_packed = self.rom.get_archive(f"data_lt2/event/ev_d{complete}.plz")
        gds_file = events_packed.open(f"e{prefix}_{postfix}.gds", "wb+")
        self.gds.write_stream(gds_file)
        gds_file.close()

    def load_texts(self):
        if self.rom is None:
            return
        prefix, postfix, complete = self.resolve_event_id()
        self.texts_archive = self.rom.get_archive(f"data_lt2/event/?/ev_t{complete}.plz".replace("?", conf.LANG))
        self.texts = {}
        event_texts = self.list_event_texts()
        for dial_id, filename in event_texts.items():
            self.texts[dial_id] = formats.gds.GDS(filename=filename, rom=self.texts_archive)

    def save_texts(self):
        prefix, postfix, complete = self.resolve_event_id()
        for dial_id, text in self.texts.items():
            text: formats.gds.GDS
            text.save(filename=f"t{prefix}_{postfix}_{dial_id}.gds", rom=self.texts_archive)

    def get_text(self, text_num):
        if self.rom is None:
            return formats.gds.GDS()
        return self.texts[text_num]

    def from_event_script(self, data: str):
        try:
            parser = event_script.EventScriptParser(data, self)
            parser.parse()
        except Exception as e:
            return False, str(e)
        return True, ""

    def list_event_texts(self):
        if self.rom is None:
            return
        text_lst = {}
        dial_files = self.texts_archive.filenames
        prefix, postfix, complete = self.resolve_event_id()
        for filename in dial_files:
            if match := re.match(f"t{prefix}_{postfix}_([0-9]+).gds", filename):
                text_lst[int(match.group(1))] = filename
        return text_lst

    def clear_event_texts(self):
        if self.rom is None:
            return
        dial_files = self.list_event_texts()
        for filename in dial_files.values():
            self.texts_archive.remove_file(filename)

    def to_readable(self):
        parser = dcc.DCCParser()
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

        EventGDSParser(ev=self).parse_into_dcc(self.gds, parser)

        return parser.serialize()

    def from_readable(self, readable):
        parser = dcc.DCCParser()
        try:
            parser.parse(readable)
        except Exception as e:
            return False, str(e)

        required_paths = ["evdat.map_top_id", "evdat.map_btm_id"]
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

        self.texts = {}

        successful, error_msg = EventGDSParser(ev=self).parse_from_dcc(self.gds, parser)

        return successful, error_msg
