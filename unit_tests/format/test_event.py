import io

import formats.event as evdat
from formats.filesystem import NintendoDSRom
from formats_parsed.dcc import DCCParser
from formats_parsed.gds_parsers.EventGDSParser import EventGDSParser
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

    def test_readable(self):
        ev, original = self.get_ev()
        ev2, original = self.get_ev()

        dcc_parser = DCCParser()
        dcc_parser.reset()
        EventGDSParser(ev).serialize_into_dcc(ev.gds, dcc_parser)
        readable = dcc_parser.serialize()

        dcc_parser.reset()
        dcc_parser.parse(readable)
        assert EventGDSParser(ev).parse_from_dcc(ev.gds, dcc_parser)[0] is True

        write_stream = io.BytesIO()
        ev.write_stream(write_stream)
        assert write_stream.getvalue() == original
        assert repr(ev.gds.params) == repr(ev2.gds.params)
        assert repr(ev.gds.commands) == repr(ev2.gds.commands)
