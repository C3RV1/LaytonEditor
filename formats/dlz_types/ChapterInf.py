from formats.dlz import Dlz
import struct


class ChapterInfEntry:
    def __init__(self, event_id: int, event_viewed_flag: int, event_id_2: int):
        self.event_id = event_id
        self.event_viewed_flag = event_viewed_flag
        self.event_id_2 = event_id_2

    @classmethod
    def from_data(cls, data: bytes):
        data = struct.unpack("<HHH", data)
        return cls(*data)

    def to_data(self) -> bytes:
        return struct.pack("<HHH", self.event_id, self.event_viewed_flag, self.event_id_2)

    def __repr__(self):
        return f"ChapterInfEntry<event_id={self.event_id}, viewed_flag={self.event_viewed_flag}," \
               f"event_id_2={self.event_id_2}>"


class ChapterInfDlz(Dlz):
    def _construct_entry_object(self, entry_data: bytes) -> ChapterInfEntry:
        return ChapterInfEntry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: ChapterInfEntry) -> bytes:
        return entry_object.to_data()

    def __getitem__(self, item: int) -> ChapterInfEntry:
        return super().__getitem__(item)

    def __setitem__(self, key: int, value: ChapterInfEntry):
        super().__setitem__(key, value)
