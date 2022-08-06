import logging
from typing import Optional

import formats.filesystem
import formats.gds
import formats.graphics.bg
import formats.dlz
import formats.parsers.dcc
from formats.binary import BinaryReader, BinaryWriter

import utility.replace_substitutions as subs
from formats import conf


class Puzzle:
    encoding = "cp1252"
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
        rdr.read_uint16()  # 112
        self.title = subs.replace_substitutions(rdr.read_string(encoding=self.encoding), True)
        rdr.seek(0x34)
        self.tutorial_id = rdr.read_uint8()
        for i in range(3):
            self.picarat_decay[i] = rdr.read_uint8()
        self._flags = rdr.read_uint8()
        self.location_id = rdr.read_uint8()
        self.type = rdr.read_uint8()
        self.bg_btm_id = rdr.read_uint8()
        rdr.read_uint16()
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
        wtr.write_uint16(112)
        wtr.write_string(subs.convert_substitutions(self.title, True), encoding=self.encoding, size=0x30)
        wtr.write_uint8(self.tutorial_id)
        for picarat in self.picarat_decay:
            wtr.write_uint8(picarat)
        wtr.write_uint8(self._flags)
        wtr.write_uint8(self.location_id)
        wtr.write_uint8(self.type)
        wtr.write_uint8(self.bg_btm_id)
        wtr.write(self.original[0x3c:0x3e])  # UnkSoundId
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

        plz: formats.filesystem.PlzArchive = rom.get_archive(f"data_lt2/nazo/?/nazo{bank}.plz".replace("?", conf.LANG))
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

        nz_lst_dlz = formats.dlz.Dlz(filename="data_lt2/rc/?/nz_lst.dlz".replace("?", conf.LANG), rom=self.rom)
        nazo_list = [list(i) for i in nz_lst_dlz.unpack("<hh48sh")]
        for item in nazo_list:
            if item[0] == self.internal_id:
                item[2] = self.pad_with_0(self.title.encode(self.encoding), 0x30)
        nz_lst_dlz.pack("<hh48sh", nazo_list)
        nz_lst_dlz.save()

        self.save_gds()

    @staticmethod
    def pad_with_0(b, length):
        res = b + b"\x00" * (length - len(b))
        res = res[:-1] + b"\x00"
        return res

    def load_gds(self):
        gds_plz_file = self.rom.get_archive("data_lt2/script/puzzle.plz")

        gds_filename = f"q{self.internal_id}_param.gds"

        if gds_filename not in gds_plz_file.filenames:
            logging.error(f"GDS for puzzle {self.internal_id} not found")
            return

        self.gds = formats.gds.GDS(gds_filename, rom=gds_plz_file)

    def save_gds(self):
        self.gds.save()
        return True

    def to_readable(self):
        parser = formats.parsers.dcc.DCCParser()
        parser.reset()
        parser.get_path("pzd", create=True)
        parser.set_named("pzd.title", self.title)
        parser.set_named("pzd.type", self.type)
        parser.set_named("pzd.number", self.number)
        parser.set_named("pzd.location_id", self.location_id)
        parser.set_named("pzd.tutorial_id", self.tutorial_id)
        parser.set_named("pzd.reward_id", self.reward_id)
        parser.set_named("pzd.bg_btm_id", self.bg_btm_id)
        parser.set_named("pzd.bg_location_id", self.bg_location_id)
        parser.set_named("pzd.judge_char", self.judge_char)
        parser.set_named("pzd.flag_bit2", self.flag_bit2)
        parser.set_named("pzd.flag_bit5", self.flag_bit5)
        parser.set_named("pzd.bg_lang", self.bg_lang)
        parser.set_named("pzd.ans_bg_lang", self.ans_bg_lang)
        parser.get_path("pzd.picarat_decay", create=True)
        for picarat in self.picarat_decay:
            parser["pzd.picarat_decay::unnamed"].append(picarat)
        parser.set_named("pzd.text", self.text)
        parser.set_named("pzd.correct_answer", self.correct_answer)
        parser.set_named("pzd.incorrect_answer", self.incorrect_answer)
        parser.set_named("pzd.hint1", self.hint1)
        parser.set_named("pzd.hint2", self.hint2)
        parser.set_named("pzd.hint3", self.hint3)

        from formats.parsers.gds_parsers import get_puzzle_gds_parser
        gds_parser = get_puzzle_gds_parser(self)
        gds_parser.parse_into_dcc(self.gds, parser)
        return parser.serialize()

    def from_readable(self, readable):
        parser = formats.parsers.dcc.DCCParser()
        try:
            parser.parse(readable)
        except Exception as e:
            return False, str(e)

        required_paths = ["pzd.title", "pzd.type", "pzd.number", "pzd.text",  "pzd.correct_answer",
                          "pzd.incorrect_answer", "pzd.hint1", "pzd.hint2", "pzd.hint3", "pzd.tutorial_id",
                          "pzd.reward_id", "pzd.bg_btm_id", "pzd.bg_location_id", "pzd.judge_char", "pzd.flag_bit2",
                          "pzd.flag_bit5", "pzd.location_id", "pzd.picarat_decay", "pzd.bg_lang", "pzd.ans_bg_lang"]

        for req_path in required_paths:
            if not parser.exists(req_path):
                return False, f"Missing {req_path}"

        self.title = parser["pzd.title"]
        self.type = parser["pzd.type"]
        self.number = parser["pzd.number"]
        self.text = parser["pzd.text"]
        self.correct_answer = parser["pzd.correct_answer"]
        self.incorrect_answer = parser["pzd.incorrect_answer"]
        self.hint1 = parser["pzd.hint1"]
        self.hint2 = parser["pzd.hint2"]
        self.hint3 = parser["pzd.hint3"]

        self.tutorial_id = parser["pzd.tutorial_id"]
        self.reward_id = parser["pzd.reward_id"]
        self.bg_btm_id = parser["pzd.bg_btm_id"]
        self.bg_location_id = parser["pzd.bg_location_id"]
        self.judge_char = parser["pzd.judge_char"]
        self.flag_bit2 = parser["pzd.flag_bit2"]
        self.flag_bit5 = parser["pzd.flag_bit5"]
        self.location_id = parser["pzd.location_id"]
        self.picarat_decay = []
        for picarat in parser["pzd.picarat_decay::unnamed"]:
            self.picarat_decay.append(picarat)

        self.bg_lang = parser["pzd.bg_lang"]
        self.ans_bg_lang = parser["pzd.ans_bg_lang"]
        self.gds.commands = []

        from formats.parsers.gds_parsers import get_puzzle_gds_parser
        gds_parser = get_puzzle_gds_parser(self)
        successful, error_msg = gds_parser.parse_from_dcc(self.gds, parser)
        return successful, error_msg

    # FLAG PROPERTIES

    @property
    def bg_lang(self):
        return (self._flags & 0x20) > 0

    @bg_lang.setter
    def bg_lang(self, value: bool):
        if value:
            self._flags |= 0x20
        else:
            self._flags &= 0xFF - 0x20

    @property
    def ans_bg_lang(self):
        return (self._flags & 0x40) > 0

    @ans_bg_lang.setter
    def ans_bg_lang(self, value: bool):
        if value:
            self._flags |= 0x40
        else:
            self._flags &= 0xFF - 0x40

    @property
    def judge_char(self):
        return self._flags & 0b11

    @judge_char.setter
    def judge_char(self, value):
        self._flags &= 0xFF - 0b11
        self._flags += value & 0b11

    @property
    def flag_bit2(self):
        return (self._flags & 0x2) > 0

    @flag_bit2.setter
    def flag_bit2(self, value):
        if value:
            self._flags |= 0x2
        else:
            self._flags &= 0xFF - 0x2

    @property
    def flag_bit5(self):
        return (self._flags & 0x10) > 0

    @flag_bit5.setter
    def flag_bit5(self, value):
        if value:
            self._flags |= 0x10
        else:
            self._flags &= 0xFF - 0x10
