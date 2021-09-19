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

    # TODO: Add working export unittest
    """
    def test_SADExport(self):
        sad_file = self.get_sadl()
        sad_data = sad_file.read()
        sad_file.close()

        sad_obj = sadl.SADL()
        sad_obj.read_stream(sad_data)

        exported_wav = sad_obj.to_wav()
        with open("test_decode.wav", "wb") as f:
            exported_wav.write_stream(f)
        with open("test_decode.wav", "rb") as f:
            exported_wav.read_stream(f)
        sad_obj.from_wav(exported_wav)
        exported_wav = sad_obj.to_wav()

        with open("test_encode.wav", "wb") as f:
            exported_wav.write_stream(f)
    """
