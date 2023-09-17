from formats.dlz import Dlz
import struct


class EventFixEntry:
    def __init__(self, unk0: int, unk1: int):
        self.unk0 = unk0
        self.unk1 = unk1

    @classmethod
    def from_data(cls, data: bytes):
        unk0, unk1 = struct.unpack("<HH", data)
        return cls(unk0, unk1)

    def to_data(self) -> bytes:
        return struct.pack("<HH", self.unk0, self.unk1)


class EventFixDlz(Dlz):
    def _construct_entry_object(self, entry_data: bytes) -> EventFixEntry:
        return EventFixEntry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: EventFixEntry) -> bytes:
        return entry_object.to_data()

    def __getitem__(self, item: int) -> EventFixEntry:
        return super().__getitem__(item)

    def __setitem__(self, key: int, value: EventFixEntry):
        super().__setitem__(key, value)
