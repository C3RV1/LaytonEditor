import unittest
from formats.filesystem import NintendoDSRom
from formats.storyflag2 import StoryFlag2
import os
import io


class TestStoryFlag2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_story_flag2(self):
        data_plz = self.rom.get_archive("/data_lt2/place/data.plz")
        with data_plz.open("storyflag2.dat", "rb") as original_f:
            original_data = original_f.read()
        return StoryFlag2(rom=data_plz, filename="storyflag2.dat"), original_data

    def test_loading_saving(self):
        story_flag2, original = self.get_story_flag2()
        story_flag2: StoryFlag2
        out_stream = io.BytesIO()
        story_flag2.write_stream(out_stream)
        assert out_stream.getvalue() == original
