import unittest
from formats.filesystem import NintendoDSRom
from formats.autoevent2 import AutoEvent2
import os
import io


class TestAutoEvent2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_auto_event2(self):
        data_plz = self.rom.get_archive("/data_lt2/place/data.plz")
        with data_plz.open("autoevent2.dat", "rb") as original_f:
            original_data = original_f.read()
        return AutoEvent2(rom=data_plz, filename="autoevent2.dat"), original_data

    def test_loading_saving(self):
        auto_event2, original = self.get_auto_event2()
        auto_event2: AutoEvent2
        out_stream = io.BytesIO()
        auto_event2.write_stream(out_stream)
        assert out_stream.getvalue() == original
