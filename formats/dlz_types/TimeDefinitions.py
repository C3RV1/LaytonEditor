from formats.dlz import Dlz
import struct


class TimeDefinitionsDlz(Dlz):
    def _construct_entry_object(self, entry_data: bytes) -> int:
        return struct.unpack("<H", entry_data)[0]

    def _serialize_entry_object(self, entry_object: int) -> bytes:
        return struct.pack("<H", entry_object)

    def __getitem__(self, item: int) -> int:
        return super().__getitem__(item)

    def __setitem__(self, key: int, value: int):
        super().__setitem__(key, value)
