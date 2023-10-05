from formats.dlz import Dlz
import struct


class NazoListEntry:
    def __init__(self, puzzle_number: int, puzzle_name: str, unk0: int):
        self.puzzle_number: int = puzzle_number
        self.puzzle_name: str = puzzle_name
        self.unk0: int = unk0

    @classmethod
    def from_data(cls, data: bytes):
        puzzle_number, puzzle_name, unk0 = struct.unpack(
            "<H48sH", data
        )
        puzzle_name: bytes
        puzzle_name: str = puzzle_name.split(b'\0')[0].decode("cp1252")
        return cls(puzzle_number, puzzle_name, unk0)

    def to_data(self) -> bytes:
        return struct.pack("<h48sh", self.puzzle_number, self.puzzle_name.encode("cp1252"), self.unk0)


class NazoListDlz(Dlz[int, NazoListEntry]):
    def _construct_entry_object(self, entry_data: bytes) -> NazoListEntry:
        return NazoListEntry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: NazoListEntry) -> bytes:
        return entry_object.to_data()
