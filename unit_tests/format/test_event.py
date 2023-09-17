import io

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
        ev.event_id = 10030
        ev.load_from_rom()

        prefix, postfix, complete = ev._resolve_event_id()
        events_packed = self.rom.get_archive(f"/data_lt2/event/ev_d{complete}.plz")
        file = events_packed.open(f"d{prefix}_{postfix}.dat", "rb")
        original = file.read()
        file.close()

        return ev, original

    def test_loading_saving(self):
        ev, original = self.get_ev()
        write_stream = io.BytesIO()
        ev.write_stream(write_stream)
        assert write_stream.getvalue() == original
