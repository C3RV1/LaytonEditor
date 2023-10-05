from formats.dlz import Dlz
import struct


class EventFixEntry:
    def __init__(self, pz_data: int, ev_viewed_flag: int):
        self.pz_data = pz_data
        self.ev_viewed_flag = ev_viewed_flag

    @classmethod
    def from_data(cls, data: bytes):
        pz_data, ev_viewed_flag = struct.unpack("<HH", data)
        return cls(pz_data, ev_viewed_flag)

    def to_data(self) -> bytes:
        return struct.pack("<HH", self.pz_data, self.ev_viewed_flag)

    def __repr__(self):
        return f"EventFixEntry<pz_data={self.pz_data}, ev_viewed_flag={self.ev_viewed_flag}>"


class EventFixDlz(Dlz[int, EventFixEntry]):
    def _construct_entry_object(self, entry_data: bytes) -> EventFixEntry:
        return EventFixEntry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: EventFixEntry) -> bytes:
        return entry_object.to_data()
