from formats.sound import smd
from formats import binary
from formats.filesystem import NintendoDSRom
import unittest
import os
import io


class TestSMD(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../../test_rom.nds")

    def get_smd(self):
        return self.rom.open("data_lt2/sound/BG_004.SMD", "rb")

    def test_SMDReadAndSave(self):
        smd_file = self.get_smd()
        smd_data = smd_file.read()
        smd_file = binary.BinaryReader(smd_file)
        smd_file.seek(0)

        smd_obj = smd.SMDL()
        smd_obj.read(smd_file)

        exported_file = io.BytesIO()
        exported_file = binary.BinaryWriter(exported_file)
        smd_obj.write(exported_file)

        exported_data = exported_file.readall()
        assert smd_data == exported_data
