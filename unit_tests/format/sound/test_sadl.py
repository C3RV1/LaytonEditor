import hashlib

from formats.sound import sadl
from formats_parsed.sound.wav import WAV
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
        # return self.rom.open("data_lt2/stream/ST_001.SAD", "rb")
        return self.rom.open("data_lt2/stream/bgm/BG_031.SAD", "rb")

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

        exported_wav, _ = WAV.from_sadl(sad_obj)
        binary_writer = binary.BinaryWriter()
        exported_wav.write_stream(binary_writer)
        assert hashlib.sha256(binary_writer.readall()).hexdigest() == "a1b342edf2eb19c5c5e3d1fcdec4d5553a13780621ba79f096b28d7750c6cc86"

        assert exported_wav.to_sadl(sad_obj) is True
        exported_wav, _ = WAV.from_sadl(sad_obj)

        binary_writer = binary.BinaryWriter()
        exported_wav.write_stream(binary_writer)
        data = binary_writer.readall()
        assert hashlib.sha256(binary_writer.readall()).hexdigest() == "f7cbf3e21d19a09f0c57873e17366ef1a99b11ce1f1097a711d7a182973f113c"
