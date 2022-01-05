import formats.gds as gds
import formats.binary as binary
from formats.filesystem import NintendoDSRom
import unittest
import os


class TestGDS(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_pzd(self):
        gds_file = gds.GDS(filename="q3_param.gds", rom=self.rom.get_archive("data_lt2/script/puzzle.plz"))
        gds_original_file = self.rom.get_archive("data_lt2/script/puzzle.plz").open("q3_param.gds", "rb")
        gds_original = gds_original_file.read()
        gds_original_file.close()
        return gds_file, gds_original

    def test_loading_saving(self):
        gds_f, gds_o = self.get_pzd()
        wtr = binary.BinaryWriter()
        gds_f.write_stream(wtr)
        assert wtr.data == gds_o
