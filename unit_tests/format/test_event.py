import formats.event as evdat
from formats.filesystem import NintendoDSRom
from formats_parsed.EventDCC import EventDCC
import unittest
import os


class TestEventData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_ev(self):
        ev = evdat.Event(rom=self.rom)
        ev.event_id = 10030
        ev.load_from_rom()
        return ev

    def test_loading_saving(self):
        pz_data = self.get_ev()
        assert pz_data.write(None) == pz_data.original

    def test_readable(self):
        pz_data = self.get_ev()
        readable = EventDCC(pz_data).serialize()
        pz_data2 = self.get_ev()
        assert EventDCC().parse(readable)[0] is True
        assert pz_data.write(None) == pz_data.original
        assert repr(pz_data.gds.params) == repr(pz_data2.gds.params)
        assert repr(pz_data.gds.commands) == repr(pz_data2.gds.commands)
