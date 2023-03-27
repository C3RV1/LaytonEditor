import logging
from typing import Optional

import formats.filesystem
import formats.gds
import formats.graphics.bg
import formats.dlz
from formats.binary import BinaryReader, BinaryWriter

import utility.replace_substitutions as subs
from formats import conf

import enum


class PuzzleType(enum.IntEnum):
    MATCHSTICK_UNUSED = 0
    UNUSED_1 = 1
    MULTIPLE_CHOICE = 2
    ON_OFF = 3
    POSITION_TO_SOLVE_UNUSED = 4
    CIRCLE_ANSWER = 5
    DRAW_LINE_PLAZA = 6  # Maybe
    CONNECT_TO_ANSWER_UNUSED = 7
    CUPS_UNUSED = 8
    LINE_DIVIDE = 9
    SORT = 0xA
    WEATHER = 0xB
    UNUSED_C = 0xC
    PILES_OF_PANCAKES = 0xD
    UNUSED_E = 0xE
    LINE_DIVIDE_LIMITED = 0xF
    WRITE_CHARS = 0x10
    KNIGHT_TOUR = 0x11
    TILE_ROTATE = 0x12
    POSITION_TO_SOLVE_UNUSED2 = 0x13
    UNUSED_14 = 0x14
    PUZZLES_172_202 = 0x15
    WRITE_NUM = 0x16
    AREA = 0x17
    ROSES = 0x18
    SLIDE = 0x19
    TILE_ROTATE_2 = 0x1A
    SLIPPERY_CROSSINGS = 0x1B
    WRITE_ALT = 0x1C
    DISAPPEARING_ACT = 0x1D
    JARS_AND_CANS = 0x1E
    LIGHT_THE_WAY = 0x1F
    PUZZLE_173 = 0x20
    RICKETY_BRIDGE = 0x21
    FIND_SHAPE = 0x22
    WRITE_DATE = 0x23


class Puzzle:
    encoding = "cp1252"

    def __init__(self, rom: formats.filesystem.NintendoDSRom = None, id_=0):
        self.rom = rom
        self.type = 0
        self.number = 0
        self.internal_id = id_
        self.tutorial_id = 0
        self.location_id = 0
        self.picarat_decay = [0, 0, 0]
        self.reward_id = 0
        self.text = ""
        self.correct_answer = ""
        self.incorrect_answer = ""
        self.hint1 = ""
        self.hint2 = ""
        self.hint3 = ""
        self.title = ""

        self.unk0 = 0
        self.unk1 = 0

        self.bg_btm_id = 0
        self.bg_location_id = 0

        self.gds = formats.gds.GDS()  # type: Optional[formats.gds.GDS]

        self._flags = 0

        self.original = b""

    def set_internal_id(self, internal_id: int):
        self.internal_id = internal_id

    def load(self, rdr):
        if not isinstance(rdr, BinaryReader):
            rdr = BinaryReader(rdr)
        rdr: BinaryReader

        self.original = rdr.read()
        rdr.seek(0)

        self.number = rdr.read_uint16()
        self.unk1 = rdr.read_uint16()  # 112
        self.title = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(0x34)
        self.tutorial_id = rdr.read_uint8()
        for i in range(3):
            self.picarat_decay[i] = rdr.read_uint8()
        self._flags = rdr.read_uint8()
        self.location_id = rdr.read_uint8()
        self.type = rdr.read_uint8()
        self.bg_btm_id = rdr.read_uint8()
        self.unk0 = rdr.read_uint16()
        self.bg_location_id = rdr.read_uint8()
        self.reward_id = rdr.read_uint8()

        puzzle_text_offset = 0x70 + rdr.read_uint32()
        puzzle_correct_answer_offset = 0x70 + rdr.read_uint32()
        puzzle_incorrect_answer_offset = 0x70 + rdr.read_uint32()
        puzzle_hint1_offset = 0x70 + rdr.read_uint32()
        puzzle_hint2_offset = 0x70 + rdr.read_uint32()
        puzzle_hint3_offset = 0x70 + rdr.read_uint32()
        rdr.seek(puzzle_text_offset)
        self.text = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(puzzle_correct_answer_offset)
        self.correct_answer = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(puzzle_incorrect_answer_offset)
        self.incorrect_answer = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(puzzle_hint1_offset)
        self.hint1 = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(puzzle_hint2_offset)
        self.hint2 = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(puzzle_hint3_offset)
        self.hint3 = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)

    def export_data(self, wtr):
        if not isinstance(wtr, BinaryWriter):
            wtr = BinaryWriter(wtr)
        wtr: BinaryWriter

        puzzle_text_section = BinaryWriter()
        puzzle_text_section.write_string(subs.convert_substitutions(self.text, puzzle=True),
                                         encoding=self.encoding)
        puzzle_correct_offset = puzzle_text_section.tell()
        puzzle_text_section.write_string(subs.convert_substitutions(self.correct_answer, puzzle=True),
                                         encoding=self.encoding)
        puzzle_incorrect_offset = puzzle_text_section.tell()
        puzzle_text_section.write_string(subs.convert_substitutions(self.incorrect_answer, puzzle=True),
                                         encoding=self.encoding)
        puzzle_hint1_offset = puzzle_text_section.tell()
        puzzle_text_section.write_string(subs.convert_substitutions(self.hint1, puzzle=True),
                                         encoding=self.encoding)
        puzzle_hint2_offset = puzzle_text_section.tell()
        puzzle_text_section.write_string(subs.convert_substitutions(self.hint2, puzzle=True),
                                         encoding=self.encoding)
        puzzle_hint3_offset = puzzle_text_section.tell()
        puzzle_text_section.write_string(subs.convert_substitutions(self.hint3, puzzle=True),
                                         encoding=self.encoding)

        wtr.write_uint16(self.number)
        wtr.write_uint16(self.unk1)  # 112
        wtr.write_string(subs.convert_substitutions(self.title, True), encoding=self.encoding, size=0x30)
        wtr.write_uint8(self.tutorial_id)
        for picarat in self.picarat_decay:
            wtr.write_uint8(picarat)
        wtr.write_uint8(self._flags)
        wtr.write_uint8(self.location_id)
        wtr.write_uint8(self.type)
        wtr.write_uint8(self.bg_btm_id)
        wtr.write_uint16(self.unk0)  # UnkSoundId
        wtr.write_uint8(self.bg_location_id)
        wtr.write_uint8(self.reward_id)

        wtr.write_uint32(0)
        wtr.write_uint32(puzzle_correct_offset)
        wtr.write_uint32(puzzle_incorrect_offset)
        wtr.write_uint32(puzzle_hint1_offset)
        wtr.write_uint32(puzzle_hint2_offset)
        wtr.write_uint32(puzzle_hint3_offset)
        wtr.write(b"\x00" * 4 * 6)
        wtr.write(puzzle_text_section.data)

        return wtr

    def get_dat_file(self, rom: formats.filesystem.NintendoDSRom, mode="rb"):
        bank = self.internal_id // 0x3c + 1
        if bank > 3:
            bank = 3

        plz: formats.filesystem.PlzArchive = rom.get_archive(f"/data_lt2/nazo/?/nazo{bank}.plz".replace("?", conf.LANG))
        if f"n{self.internal_id}.dat" not in plz.filenames:
            logging.error(f"Nazo dat not found (internal id {self.internal_id})")
            return None

        return plz.open(f"n{self.internal_id}.dat", mode)

    def load_from_rom(self):
        dat_file = self.get_dat_file(self.rom, mode="rb")
        if dat_file is None:
            return False
        self.load(dat_file)
        dat_file.close()
        self.load_gds()
        return True

    @staticmethod
    def load_str(b, offset):
        ret = b""
        while b[offset] != 0:
            ret += bytes([b[offset]])
            offset += 1
        return ret

    def save_to_rom(self):
        dat_file = self.get_dat_file(self.rom, mode="wb")
        self.export_data(dat_file)
        dat_file.close()

        nz_lst_dlz = formats.dlz.NazoListDlz(filename=f"data_lt2/rc/{conf.LANG}/nz_lst.dlz", rom=self.rom)
        nz_lst_dlz[self.internal_id] = self.pad_with_0(self.title.encode(self.encoding), 0x30)
        nz_lst_dlz.save()

        self.save_gds()

    @staticmethod
    def pad_with_0(b, length):
        res = b + b"\x00" * (length - len(b))
        res = res[:-1] + b"\x00"
        return res

    def load_gds(self):
        gds_plz_file = self.rom.get_archive("/data_lt2/script/puzzle.plz")

        gds_filename = f"q{self.internal_id}_param.gds"

        if gds_filename not in gds_plz_file.filenames:
            logging.error(f"GDS for puzzle {self.internal_id} not found")
            return

        self.gds = formats.gds.GDS(gds_filename, rom=gds_plz_file)

    def save_gds(self):
        self.gds.save()
        return True

    # FLAG PROPERTIES

    @property
    def bg_lang(self):
        return (self._flags & 0x20) > 0

    @bg_lang.setter
    def bg_lang(self, value: bool):
        self._flags &= ~0x20
        if value:
            self._flags |= 0x20

    @property
    def ans_bg_lang(self):
        return (self._flags & 0x40) > 0

    @ans_bg_lang.setter
    def ans_bg_lang(self, value: bool):
        self._flags &= ~0x40
        if value:
            self._flags |= 0x40

    @property
    def judge_char(self):
        return self._flags & 0b11

    @judge_char.setter
    def judge_char(self, value):
        self._flags &= ~0b11
        self._flags += value & 0b11

    @property
    def flag_bit2(self):
        return (self._flags & 0x2) > 0

    @flag_bit2.setter
    def flag_bit2(self, value):
        self._flags &= ~0x2
        if value:
            self._flags |= 0x2

    # MAYBE WHETHER THE PUZZLE HAS ANSWER IMAGE
    @property
    def has_answer_bg(self):
        return (self._flags & 0x10) > 0

    @has_answer_bg.setter
    def has_answer_bg(self, value):
        self._flags &= ~0x10
        if value:
            self._flags |= 0x10
