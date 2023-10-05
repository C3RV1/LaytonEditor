from formats.dlz import Dlz
import struct


class SoundFixEntry:
    def __init__(self, music_id: int, unk0: int, unk1: int):
        self.music_id: int = music_id
        self.unk0: int = unk0
        self.unk1: int = unk1

    @classmethod
    def from_data(cls, data: bytes):
        music_id, unk0, unk1 = struct.unpack(
            "<HHH", data
        )
        return cls(music_id, unk0, unk1)

    def to_data(self) -> bytes:
        return struct.pack("<HHH", self.music_id, self.unk0, self.unk1)


class SoundFixDlz(Dlz[int, SoundFixEntry]):
    def _construct_entry_object(self, entry_data: bytes) -> SoundFixEntry:
        return SoundFixEntry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: SoundFixEntry) -> bytes:
        return entry_object.to_data()
