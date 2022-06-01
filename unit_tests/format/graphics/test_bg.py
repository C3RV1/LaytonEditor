import io

from formats.graphics.bg import BGImage
from formats import binary
from formats.filesystem import NintendoDSRom, CompressedIOWrapper
import unittest
import os


class TestBGImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(os.path.join(rom_path, "../../../test_rom.nds"))

    def get_bg(self):
        file = self.rom.open("data_lt2/bg/map/main0.arc", "rb")
        file = CompressedIOWrapper(file, double_typed=True)
        return file

    def test_BGReadAndSave(self):
        bg_file = self.get_bg()
        bg_data = bg_file.read()
        bg_file.close()

        bg_obj = BGImage(filename="data_lt2/bg/map/main0.arc", rom=self.rom)

        exported_file = io.BytesIO()
        exported_file = binary.BinaryWriter(exported_file)
        bg_obj.write_stream(exported_file)

        exported_data = exported_file.readall()
        assert bg_data == exported_data
