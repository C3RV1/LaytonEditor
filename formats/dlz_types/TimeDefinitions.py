from formats.dlz import Dlz
import struct


class TimeDefinitionsDlz(Dlz[int, int]):
    def _construct_entry_object(self, entry_data: bytes) -> int:
        return struct.unpack("<H", entry_data)[0]

    def _serialize_entry_object(self, entry_object: int) -> bytes:
        return struct.pack("<H", entry_object)
