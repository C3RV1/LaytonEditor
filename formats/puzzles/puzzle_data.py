import struct

from typing import Optional

import formats.filesystem
import formats.gds
import formats.graphics.bg
import formats.dlz
import formats.dcc_parser
import formats.puzzles.puzzle_gds_parser as pz_gds


class PuzzleData:
    UNUSED_0 = 0
    UNUSED_1 = 1
    MULTIPLE_CHOICE = 2
    MARK_ANSWER = 3
    UNUSED_4 = 4
    CIRCLE_ANSWER = 5
    DRAW_LINE_PLAZA = 6  # Maybe
    UNUSED_7 = 7
    UNUSED_8 = 8
    LINE_DIVIDE = 9
    SORT = 0xA
    WEATHER = 0xB
    UNUSED_C = 0xC
    PILES_OF_PANCAKES = 0xD
    UNUSED_E = 0xE
    LINE_DIVIDE_LIMITED = 0xF
    INPUT_CHARACTERS = 0x10
    KNIGHT_TOUR = 0x11
    TILE_ROTATE = 0x12
    UNUSED_13 = 0x13
    UNUSED_14 = 0x14
    UNACCESSIBLE_172_202 = 0x15
    INPUT_NUMERIC = 0x16
    AREA = 0x17
    ROSES = 0x18
    SLIDE = 0x19
    TILE_ROTATE_2 = 0x1A
    SLIPPERY_CROSSINGS = 0x1B
    INPUT_ALTERNATIVE = 0x1C
    DISAPPEARING_ACT = 0x1D
    JARS_AND_CANS = 0x1E
    LIGHT_THE_WAY = 0x1F
    UNACCESSIBLE_173 = 0x20
    RICKETY_BRIDGE = 0x21
    FIND_SHAPE = 0x22
    INPUT_DATE = 0x23

    INPUTS = [INPUT_DATE, INPUT_NUMERIC, INPUT_ALTERNATIVE, INPUT_CHARACTERS]

    TYPE_TO_GDS_PARSER = {
        INPUT_DATE: pz_gds.InputGDSParser,
        INPUT_NUMERIC: pz_gds.InputGDSParser,
        INPUT_ALTERNATIVE: pz_gds.InputGDSParser,
        INPUT_CHARACTERS: pz_gds.InputGDSParser,
        MULTIPLE_CHOICE: pz_gds.MultipleChoiceGDSParser
    }

    def __init__(self, rom: formats.filesystem.NintendoDSRom = None):
        self.rom = rom
        self.type = 0
        self.number = 0
        self.internal_id = 0
        self.location = 0
        self.text = b""
        self.correct_answer = b""
        self.incorrect_answer = b""
        self.hint1 = b""
        self.hint2 = b""
        self.hint3 = b""
        self.title = b""
        self.bg = None  # type: Optional[formats.graphics.bg.BGImage]

        self.gds = None  # type: Optional[formats.gds.GDS]

        self._flags = 0

        self.original = b""

    def set_internal_id(self, internal_id: int):
        self.internal_id = internal_id

    def load(self, b: bytes):
        self.original = b

        self.type = b[0x3a]
        puzzle_text_offset = 0x70 + struct.unpack("<i", b[0x40:0x44])[0]
        self.text = self.load_str(b, puzzle_text_offset)
        puzzle_correct_answer_offset = 0x70 + struct.unpack("<i", b[0x44:0x48])[0]
        self.correct_answer = self.load_str(b, puzzle_correct_answer_offset)
        puzzle_incorrect_answer_offset = 0x70 + struct.unpack("<i", b[0x48:0x4c])[0]
        self.incorrect_answer = self.load_str(b, puzzle_incorrect_answer_offset)
        puzzle_hint1_offset = 0x70 + struct.unpack("<i", b[0x4c:0x50])[0]
        self.hint1 = self.load_str(b, puzzle_hint1_offset)
        puzzle_hint2_offset = 0x70 + struct.unpack("<i", b[0x50:0x54])[0]
        self.hint2 = self.load_str(b, puzzle_hint2_offset)
        puzzle_hint3_offset = 0x70 + struct.unpack("<i", b[0x54:0x58])[0]
        self.hint3 = self.load_str(b, puzzle_hint3_offset)
        self.title = self.load_str(b, 0x4)
        self.number = struct.unpack("<h", b[0x0:0x2])[0]
        self.location = b[0x3e]

        self._flags = b[0x38]

    def get_dat_file(self, rom: formats.filesystem.NintendoDSRom):
        if rom.name == b'LAYTON1' and False:
            _folder: str = rom.filenames["data/ani"]
        elif rom.name == b'LAYTON2':
            _folder: str = rom.filenames["data_lt2/nazo/en"]
        else:
            print(f"Could get images for: {rom.name}")
            return False, ""

        bank = self.internal_id // 0x3c + 1
        if bank > 3:
            bank = 3

        plz = rom.get_archive(f"data_lt2/nazo/en/nazo{bank}.plz")
        if f"n{self.internal_id}.dat" not in plz.filenames:
            print("Nazo dat not found")
            return False, ""

        return plz, plz.filenames.index(f"n{self.internal_id}.dat")

    def load_from_rom(self):
        dat_files, index = self.get_dat_file(self.rom)
        if dat_files is False:
            return False
        dat_file = dat_files.files[index]
        self.load(dat_file)
        self.load_bg_from_rom()
        self.load_gds()
        return True

    def load_bg_from_rom(self):
        bg_id = self.rom.filenames.idOf(self.bg_path)
        if bg_id is None:
            print(f"Warning: bg for puzzle {self.internal_id} not found")
            self.bg = None
            return
        self.bg = formats.graphics.bg.BGImage(self.bg_path, rom=self.rom)

    @property
    def bg_path(self):
        if not self.bg_lang_dependant:
            file_name = "q{}.arc".format(self.internal_id)
        else:
            file_name = "en/q{}.arc".format(self.internal_id)
        return f"data_lt2/bg/nazo/{file_name}"

    @staticmethod
    def load_str(b, offset):
        ret = b""
        while b[offset] != 0:
            ret += bytes([b[offset]])
            offset += 1
        return ret

    @property
    def bg_lang_dependant(self):
        return (self._flags & 0x20) > 0

    @bg_lang_dependant.setter
    def bg_lang_dependant(self, value: bool):
        if value:
            self._flags |= 0x20
        else:
            self._flags &= 0xFF - 0x20

    @property
    def ans_bg_lang_dependant(self):
        return (self._flags & 0x40) > 0

    @ans_bg_lang_dependant.setter
    def ans_bg_lang_dependant(self, value: bool):
        if value:
            self._flags |= 0x40
        else:
            self._flags &= 0xFF - 0x40

    def export_data(self):
        puzzle_text_section = b""
        puzzle_text_section += self.text + b"\x00"
        puzzle_correct_offset = len(puzzle_text_section)
        puzzle_text_section += self.correct_answer + b"\x00"
        puzzle_incorrect_offset = len(puzzle_text_section)
        puzzle_text_section += self.incorrect_answer + b"\x00"
        puzzle_hint1_offset = len(puzzle_text_section)
        puzzle_text_section += self.hint1 + b"\x00"
        puzzle_hint2_offset = len(puzzle_text_section)
        puzzle_text_section += self.hint2 + b"\x00"
        puzzle_hint3_offset = len(puzzle_text_section)
        puzzle_text_section += self.hint3 + b"\x00"

        result = struct.pack("<h", self.number)
        result += struct.pack("<h", 112)
        result += self.pad_with_0(self.title, 0x30)
        result += self.original[0x34:0x38]
        result += bytes([self._flags])
        result += self.original[0x39:0x3a]
        result += bytes([self.type])
        result += bytes([self.internal_id])
        # TODO: Add puzzle location (0x3e)
        result += self.original[0x3c:0x40]
        result += struct.pack("<iiiiii", 0, puzzle_correct_offset, puzzle_incorrect_offset, puzzle_hint1_offset,
                              puzzle_hint2_offset, puzzle_hint3_offset)
        result += (b"\x00" * 4) * 6
        result += puzzle_text_section

        return result

    def save_to_rom(self):
        dat_files, dat_index = self.get_dat_file(self.rom)
        dat_files.files[dat_index] = self.export_data()
        dat_files.save()

        nz_lst_dlz = formats.dlz.Dlz(filename="data_lt2/rc/en/nz_lst.dlz", rom=self.rom)
        nazo_list = [list(i) for i in nz_lst_dlz.unpack("<hh48sh")]
        for item in nazo_list:
            print(item)
            if item[0] == self.internal_id:
                item[2] = self.pad_with_0(self.title, 0x30)
        nz_lst_dlz.pack("<hh48sh", nazo_list)
        nz_lst_dlz.save()

    @staticmethod
    def pad_with_0(b, length):
        res = b + b"\x00" * (length - len(b))
        res = res[:-1] + b"\x00"
        return res

    def load_gds(self):
        gds_plz_file = self.rom.get_archive("data_lt2/script/puzzle.plz")

        gds_filename = f"q{self.internal_id}_param.gds"

        if gds_filename not in gds_plz_file.filenames:
            return False

        self.gds = formats.gds.GDS(gds_filename, rom=gds_plz_file)
        return True

    def save_gds(self):
        gds_plz_file = self.rom.get_archive("data_lt2/script/puzzle.plz")

        gds_filename = "q{}_param.gds".format(self.internal_id)

        self.gds.save(gds_filename, rom=gds_plz_file)
        return True

    def get_gds_parser(self):
        if self.type in self.TYPE_TO_GDS_PARSER:
            return self.TYPE_TO_GDS_PARSER[self.type]()
        return pz_gds.PuzzleGDSParser()

    def to_readable(self):
        parser = formats.dcc_parser.Parser()
        parser.reset()
        parser.get_path("puzzle_data", create=True)
        parser.set_named("puzzle_data.title", self.title.decode("ascii"))
        parser.set_named("puzzle_data.type", self.type)
        parser.set_named("puzzle_data.number", self.number)
        parser.set_named("puzzle_data.location", self.location)
        parser.set_named("puzzle_data.bg_lang_dependant", self.bg_lang_dependant)
        parser.set_named("puzzle_data.ans_lang_dependant", self.ans_bg_lang_dependant)
        parser.set_named("puzzle_data.text", self.text.decode("ascii"))
        parser.set_named("puzzle_data.correct_answer", self.correct_answer.decode("ascii"))
        parser.set_named("puzzle_data.incorrect_answer", self.incorrect_answer.decode("ascii"))
        parser.set_named("puzzle_data.hint1", self.hint1.decode("ascii"))
        parser.set_named("puzzle_data.hint2", self.hint2.decode("ascii"))
        parser.set_named("puzzle_data.hint3", self.hint3.decode("ascii"))
        parser.get_path("puzzle_gds", create=True)
        gds_parser = self.get_gds_parser()
        for command in self.gds.commands:
            parser["puzzle_gds::calls"].append({
                "func": gds_parser.parse_command_name(command),
                "parameters": command.params
            })
        return parser.serialize()

    def from_readable(self, readable):
        parser = formats.dcc_parser.Parser()
        parser.parse(readable)
        self.title = parser["puzzle_data.title"]
        self.type = parser["puzzle_data.type"]
        self.number = parser["puzzle_data.number"]
        self.location = parser["puzzle_data.location"]
        self.text = parser["puzzle_data.text"]
        self.correct_answer = parser["puzzle_data.correct_answer"]
        self.incorrect_answer = parser["puzzle_data.incorrect_answer"]
        self.hint1 = parser["puzzle_data.hint1"]
        self.hint2 = parser["puzzle_data.hint2"]
        self.hint3 = parser["puzzle_data.hint3"]
        self.bg_lang_dependant = parser["puzzle_data.bg_land_dependant"]
        self.ans_bg_lang_dependant = parser["puzzle_data.ans_bg_lang_dependant"]
        self.gds.commands = []
        gds_parser = self.get_gds_parser()
        for command_call in parser["puzzle_gds::calls"]:
            self.gds.commands.append(formats.gds.GDSCommand(
                command=gds_parser.reverse_command_name(command_call["func"]),
                params=command_call["params"]
            ))
        pass
