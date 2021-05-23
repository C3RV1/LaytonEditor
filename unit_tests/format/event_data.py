import formats.event as evdat
from formats.filesystem import NintendoDSRom
import unittest
import os


class TestEventData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_ev(self):
        ev = evdat.Event(rom=self.rom)
        ev.set_event_id(14230)
        ev.load_from_rom()
        return ev

    def test_loading_saving(self):
        pz_data = self.get_ev()
        print(pz_data.write(None))
        print(pz_data.original)
        assert pz_data.write(None) == pz_data.original

    def test_readable(self):
        pz_data = self.get_ev()
        readable = pz_data.to_readable()
        assert pz_data.from_readable(readable)[0] is True
        assert pz_data.write(None) == pz_data.original
