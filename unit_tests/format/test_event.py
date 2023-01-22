import io

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

        prefix, postfix, complete = ev._resolve_event_id()
        events_packed = self.rom.get_archive(f"/data_lt2/event/ev_d{complete}.plz")
        file = events_packed.open(f"d{prefix}_{postfix}.dat", "rb")
        original = file.read()
        file.close()

        return ev, original

    def test_loading_saving(self):
        pz_data, original = self.get_ev()
        write_stream = io.BytesIO()
        pz_data.write_stream(write_stream)
        assert write_stream.getvalue() == original

    def test_readable(self):
        pz_data, original = self.get_ev()
        readable = EventDCC(pz_data).serialize()
        pz_data2, original = self.get_ev()
        assert EventDCC().parse(readable)[0] is True
        write_stream = io.BytesIO()
        pz_data.write_stream(write_stream)
        assert write_stream.getvalue() == original
        assert repr(pz_data.gds.params) == repr(pz_data2.gds.params)
        assert repr(pz_data.gds.commands) == repr(pz_data2.gds.commands)
