import io

from formats.graphics.ani import AniSprite
from formats import binary
from formats.filesystem import NintendoDSRom, CompressedIOWrapper
import unittest
import os
import hashlib


class TestAniSprite(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(os.path.join(rom_path, "../../../test_rom.nds"))

    def test_AniReadAndSave(self):
        ani_obj = AniSprite(filename="data_lt2/ani/eventchr/chr1.arc", rom=self.rom)

        exported_file = io.BytesIO()
        exported_file = binary.BinaryWriter(exported_file)
        ani_obj.write_stream(exported_file)

        exported_data = exported_file.readall()
        # The original ani data has an issue with the anim names
        # Can't check exact data, check hash
        assert hashlib.md5(exported_data).hexdigest() == "23c7a5575c7fd8f76b301442f139a577"
