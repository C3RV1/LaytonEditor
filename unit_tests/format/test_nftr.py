import formats.nftr as nftr
import formats.binary as binary
from formats.filesystem import NintendoDSRom
import unittest
import os


class TestNFTR(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_pzd(self):
        nftr_file = nftr.NFTR(filename="data_lt2/font/fontevent.NFTR", rom=self.rom)
        nftr_original_file = self.rom.open("data_lt2/font/fontevent.NFTR", "rb")
        nftr_original = nftr_original_file.read()
        nftr_original_file.close()
        return nftr_file, nftr_original

    def test_loading_saving(self):
        nftr_f, nftr_o = self.get_pzd()
        wtr = binary.BinaryWriter()
        nftr_f.write_stream(wtr)
        assert wtr.data == nftr_o