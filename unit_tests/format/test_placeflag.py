import unittest
from formats.filesystem import NintendoDSRom
from formats.placeflag import PlaceFlag
import os
import io


class TestPlaceFlag(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_place_flag(self):
        data_plz = self.rom.get_archive("/data_lt2/place/data.plz")
        with data_plz.open("placeflag.dat", "rb") as original_f:
            original_data = original_f.read()
        return PlaceFlag(rom=data_plz, filename="placeflag.dat"), original_data

    def test_loading_saving(self):
        story_flag2, original = self.get_place_flag()
        story_flag2: PlaceFlag
        out_stream = io.BytesIO()
        story_flag2.write_stream(out_stream)
        assert out_stream.getvalue() == original
