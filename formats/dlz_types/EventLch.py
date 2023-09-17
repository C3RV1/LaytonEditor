from formats.dlz import Dlz
import struct


class EventLchEntry:
    def __init__(self, unk0: int, event_name: str):
        self.unk0: int = unk0
        self.event_name: str = event_name

    @classmethod
    def from_data(cls, data: bytes):
        unk0, event_name = struct.unpack(
            "<H48s", data
        )
        event_name: bytes
        event_name: str = event_name.split(b'\0')[0].decode("shift-jis")  # TODO: Check if it is shift-jis
        return cls(unk0, event_name)

    def to_data(self) -> bytes:
        return struct.pack("<H48s", self.unk0, self.event_name.encode("shift-jis"))


class EventLchDlz(Dlz):
    def _construct_entry_object(self, entry_data: bytes) -> EventLchEntry:
        return EventLchEntry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: EventLchEntry) -> bytes:
        return entry_object.to_data()

    def __getitem__(self, item: int) -> EventLchEntry:
        return super().__getitem__(item)

    def __setitem__(self, key: int, value: EventLchEntry):
        super().__setitem__(key, value)
