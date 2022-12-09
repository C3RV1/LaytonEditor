from formats.event import Event
from formats_parsed.dcc import DCCParser
from formats_parsed.gds_parsers.EventGDSParser import EventGDSParser


class EventDCC:
    def __init__(self, ev=None):
        self.ev = ev
        if self.ev is None:
            self.ev = Event()

        self.parser = DCCParser()

    def parse(self, data: str):
        self.parser.reset()
        try:
            self.parser.parse(data)
        except Exception as e:
            return False, str(e)

        required_paths = ["evdat.map_top_id", "evdat.map_btm_id"]
        for i in range(8):
            required_paths.extend([f"evdat.char{i}.char", f"evdat.char{i}.pos", f"evdat.char{i}.shown",
                                   f"evdat.char{i}.anim"])

        for req_path in required_paths:
            if not self.parser.exists(req_path):
                return False, f"Missing {req_path}"

        self.ev.map_top_id = self.parser["evdat.map_top_id"]
        self.ev.map_bottom_id = self.parser["evdat.map_btm_id"]

        for i in range(8):
            self.ev.characters[i] = self.parser[f"evdat.char{i}.char"]
            self.ev.characters_pos[i] = self.parser[f"evdat.char{i}.pos"]
            self.ev.characters_shown[i] = self.parser[f"evdat.char{i}.shown"]
            self.ev.characters_anim_index[i] = self.parser[f"evdat.char{i}.anim"]

        self.ev.texts = {}

        successful, error_msg = EventGDSParser(ev=self.ev).parse_from_dcc(self.ev.gds, self.parser)

        return successful, error_msg

    def serialize(self):
        self.parser.reset()
        self.parser.get_path("evdat", create=True)
        self.parser.set_named("evdat.map_top_id", self.ev.map_top_id)
        self.parser.set_named("evdat.map_btm_id", self.ev.map_bottom_id)
        for i in range(len(self.ev.characters)):
            self.parser.get_path(f"evdat.char{i}", create=True)
            self.parser.set_named(f"evdat.char{i}.char", self.ev.characters[i])
            self.parser.set_named(f"evdat.char{i}.pos", self.ev.characters_pos[i])
            self.parser.set_named(f"evdat.char{i}.shown", self.ev.characters_shown[i])
            self.parser.set_named(f"evdat.char{i}.anim", self.ev.characters_anim_index[i])

        EventGDSParser(ev=self.ev).parse_into_dcc(self.ev.gds, self.parser)

        return self.parser.serialize()
