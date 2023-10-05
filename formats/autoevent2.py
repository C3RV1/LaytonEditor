from formats.filesystem import FileFormat
from formats.binary import BinaryReader, BinaryWriter
from typing import BinaryIO


class AutoEvent2Entry:
    def __init__(self, event_id: int, story_step_lower_bound: int,
                 story_step_upper_bound: int, unk0: int):
        self.event_id = event_id
        self.story_step_lower_bound = story_step_lower_bound
        self.story_step_upper_bound = story_step_upper_bound
        self.unk0 = unk0  # Always 0
        assert unk0 == 0

    @classmethod
    def read_stream(cls, rdr: BinaryReader):
        return cls(rdr.read_uint16(), rdr.read_uint16(), rdr.read_uint16(), rdr.read_uint16())

    def write_stream(self, wtr: BinaryWriter):
        wtr.write_uint16(self.event_id)
        wtr.write_uint16(self.story_step_lower_bound)
        wtr.write_uint16(self.story_step_upper_bound)
        wtr.write_uint16(self.unk0)

    def __repr__(self):
        return f"AutoEvent2Entry<ev={self.event_id}, story_step_range=[{self.story_step_lower_bound}," \
               f"{self.story_step_upper_bound}]>"


class AutoEvent2Place(list[AutoEvent2Entry]):
    @classmethod
    def read_stream(cls, rdr: BinaryReader):
        ret = cls()
        for _ in range(8):
            entry = AutoEvent2Entry.read_stream(rdr)
            if entry.event_id == 0:
                continue
            ret.append(entry)
        return ret

    def write_stream(self, wtr: BinaryWriter):
        if len(self) > 8:
            raise ValueError("AutoEvent2 Place must have 8 entries.")
        for entry in self:
            entry: AutoEvent2Entry
            entry.write_stream(wtr)
        for _ in range(8 - len(self)):
            entry = AutoEvent2Entry(0, 0, 0, 0)
            entry.write_stream(wtr)


class AutoEvent2(FileFormat, list[AutoEvent2Place]):
    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        self.clear()
        for _ in range(128):
            self.append(AutoEvent2Place.read_stream(rdr))

    def write_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)
        if len(self) != 128:
            raise ValueError("AutoEvent2 must have 128 places.")
        for place in self:
            place: AutoEvent2Place
            place.write_stream(wtr)

