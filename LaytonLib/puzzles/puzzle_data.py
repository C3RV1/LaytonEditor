import struct
import ndspy.rom
import LaytonLib.filesystem
import LaytonLib.images.bg
import wx


class PuzzleData:
    def __init__(self):
        self.puzzle_type = 0
        self.puzzle_number = 0
        self.puzzle_internal_id = 0
        self.puzzle_location = 0
        self.puzzle_text = b""
        self.puzzle_correct_answer = b""
        self.puzzle_incorrect_answer = b""
        self.puzzle_hint1 = b""
        self.puzzle_hint2 = b""
        self.puzzle_hint3 = b""
        self.puzzle_title = b""
        self.puzzle_bg = None  # type: LaytonLib.images.bg.BgFile
        self.puzzle_bg_bitmap = None  # type: wx.Bitmap

        self._puzzle_flags = 0

        self.puzzle_original = b""

    def set_internal_id(self, internal_id: int):
        self.puzzle_internal_id = internal_id

    def load(self, b: bytes):
        self.puzzle_original = b

        self.puzzle_type = b[0x3a]
        puzzle_text_offset = 0x70 + struct.unpack("<i", b[0x40:0x44])[0]
        self.puzzle_text = self.load_str(b, puzzle_text_offset)
        puzzle_correct_answer_offset = 0x70 + struct.unpack("<i", b[0x44:0x48])[0]
        self.puzzle_correct_answer = self.load_str(b, puzzle_correct_answer_offset)
        puzzle_incorrect_answer_offset = 0x70 + struct.unpack("<i", b[0x48:0x4c])[0]
        self.puzzle_incorrect_answer = self.load_str(b, puzzle_incorrect_answer_offset)
        puzzle_hint1_offset = 0x70 + struct.unpack("<i", b[0x4c:0x50])[0]
        self.puzzle_hint1 = self.load_str(b, puzzle_hint1_offset)
        puzzle_hint2_offset = 0x70 + struct.unpack("<i", b[0x50:0x54])[0]
        self.puzzle_hint2 = self.load_str(b, puzzle_hint2_offset)
        puzzle_hint3_offset = 0x70 + struct.unpack("<i", b[0x54:0x58])[0]
        self.puzzle_hint3 = self.load_str(b, puzzle_hint3_offset)
        self.puzzle_title = self.load_str(b, 0x4)
        self.puzzle_number = struct.unpack("<h", b[0x0:0x2])[0]

        self._puzzle_flags = b[0x38]

    def get_dat_file(self, rom: ndspy.rom.NintendoDSRom):
        if rom.name == b'LAYTON1' and False:
            folder: str = rom.filenames["data/ani"]
        elif rom.name == b'LAYTON2':
            folder: str = rom.filenames["data_lt2/nazo"]
        else:
            print(f"Could get images for: {rom.name}")
            return False

        filenames_to_id = {}
        for line in str(folder).split("\n"):
            filenames_to_id[line.split(" ")[-1]] = int(line.split(" ")[0])

        if self.puzzle_internal_id < 0x3c:
            load_id = filenames_to_id["nazo1.plz"]
        elif self.puzzle_internal_id < 0x78:
            load_id = filenames_to_id["nazo2.plz"]
        else:
            load_id = filenames_to_id["nazo3.plz"]

        plz = LaytonLib.filesystem.PlzFile(rom, load_id)
        if "n{}.dat".format(self.puzzle_internal_id) not in plz.filenames:
            print("Nazo dat not found")
            return False

        return plz, plz.filenames.index("n{}.dat".format(self.puzzle_internal_id))

    def load_from_rom(self, rom: ndspy.rom.NintendoDSRom):
        dat_files, index = self.get_dat_file(rom)
        dat_file = dat_files.files[index]
        self.load(dat_file)
        self.load_bg_from_rom(rom)
        return True

    def load_bg_from_rom(self, rom: ndspy.rom.NintendoDSRom):
        if not self.puzzle_bg_lang_dependant:
            file_name = "q{}.arc".format(self.puzzle_internal_id)
        else:
            file_name = "en/q{}.arc".format(self.puzzle_internal_id)
        bg_id = rom.filenames.idOf("data_lt2/bg/nazo/{}".format(file_name))
        self.puzzle_bg = LaytonLib.images.bg.BgFile(rom, bg_id)

    def load_str(self, b, offset):
        ret = b""
        while b[offset] != 0:
            ret += bytes([b[offset]])
            offset += 1
        return ret

    @property
    def puzzle_bg_lang_dependant(self):
        return (self._puzzle_flags & 0x20) > 0

    @puzzle_bg_lang_dependant.setter
    def puzzle_bg_lang_dependant(self, value: bool):
        if value:
            self._puzzle_flags |= 0x20
        else:
            self._puzzle_flags &= 0xFF - 0x20

    @property
    def puzzle_answer_bg_lang_dependant(self):
        return (self._puzzle_flags & 0x40) > 0

    @puzzle_answer_bg_lang_dependant.setter
    def puzzle_answer_bg_lang_dependant(self, value: bool):
        if value:
            self._puzzle_flags |= 0x40
        else:
            self._puzzle_flags &= 0xFF - 0x40

    def export_data(self):
        puzzle_text_section = b""
        puzzle_text_section += self.puzzle_text + b"\x00"
        puzzle_correct_offset = len(puzzle_text_section)
        puzzle_text_section += self.puzzle_correct_answer + b"\x00"
        puzzle_incorrect_offset = len(puzzle_text_section)
        puzzle_text_section += self.puzzle_incorrect_answer + b"\x00"
        puzzle_hint1_offset = len(puzzle_text_section)
        puzzle_text_section += self.puzzle_hint1 + b"\x00"
        puzzle_hint2_offset = len(puzzle_text_section)
        puzzle_text_section += self.puzzle_hint2 + b"\x00"
        puzzle_hint3_offset = len(puzzle_text_section)
        puzzle_text_section += self.puzzle_hint3 + b"\x00"

        result = struct.pack("<h", self.puzzle_number)
        result += struct.pack("<h", 112)
        result += self.pad_with_0(self.puzzle_title, 0x30)
        result += self.puzzle_original[0x34:0x38]
        result += bytes([self._puzzle_flags])
        result += self.puzzle_original[0x39:0x3a]
        result += bytes([self.puzzle_type])
        result += bytes([self.puzzle_internal_id])
        # TODO: Add puzzle location (0x3e)
        result += self.puzzle_original[0x3c:0x40]
        result += struct.pack("<iiiiii", 0, puzzle_correct_offset, puzzle_incorrect_offset, puzzle_hint1_offset,
                              puzzle_hint2_offset, puzzle_hint3_offset)
        result += (b"\x00"*4)*6
        result += puzzle_text_section

        return result

    def save_to_rom(self, rom):
        dat_files, dat_index = self.get_dat_file(rom)
        dat_files.files[dat_index] = self.export_data()
        dat_files.save()

    def pad_with_0(self, b, length):
        res = b + b"\x00"*(length - len(b))
        res = res[:-1] + b"\x00"
        return res

