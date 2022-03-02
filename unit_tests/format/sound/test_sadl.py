import hashlib

from formats.sound import sadl
from formats import binary
from formats.filesystem import NintendoDSRom
import unittest
import os
import io


class TestSADL(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../../test_rom.nds")

    def get_sadl(self):
        return self.rom.open("data_lt2/stream/ST_001.SAD", "rb")

    def test_SADReadAndSave(self):
        sad_file = self.get_sadl()
        sad_data = sad_file.read()
        sad_file.close()

        sad_obj = sadl.SADL()
        sad_obj.read_stream(sad_data)

        exported_file = io.BytesIO()
        exported_file = binary.BinaryWriter(exported_file)
        sad_obj.write_stream(exported_file)

        exported_data = exported_file.readall()

        assert sad_data == exported_data

    def test_SADExport(self):
        sad_file = self.get_sadl()
        sad_data = sad_file.read()
        sad_file.close()

        sad_obj = sadl.SADL()
        sad_obj.read_stream(sad_data)

        exported_wav = sad_obj.to_wav()
        binary_writer = binary.BinaryWriter()
        exported_wav.write_stream(binary_writer)
        assert hashlib.sha256(binary_writer.readall()).digest() == b'\xa1\xb3B\xed\xf2\xeb\x19\xc5\xc5\xe3\xd1\xfc\xde\xc4\xd5U:\x13x\x06!\xbay\xf0\x96\xb2\x8dwP\xc6\xcc\x86'

        sad_obj.from_wav(exported_wav)
        exported_wav = sad_obj.to_wav()

        binary_writer = binary.BinaryWriter()
        exported_wav.write_stream(binary_writer)
        assert hashlib.sha256(binary_writer.readall()).digest() == b'\xf7\xcb\xf3\xe2\x1d\x19\xa0\x9f\x0cW\x87>\x176n\xf1\xa9\x9b\x11\xce\x1f\x10\x97\xa7\x11\xd7\xa1\x82\x97?\x11<'
