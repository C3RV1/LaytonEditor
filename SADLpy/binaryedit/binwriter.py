# By Cervi for Team Top Hat

from typing import BinaryIO
import struct
from os import SEEK_END


class BinaryWriter:
    def __init__(self, buf: BinaryIO, endian: str = "<"):
        self.buf = buf
        self.endian = endian

    def seek(self, *args) -> int:
        return self.buf.seek(*args)

    def tell(self) -> int:
        return self.buf.tell()

    def write_string(self, string: str):
        self.buf.write(string.encode("utf-16"))

    def write_bool(self, bool_: bool):
        self.buf.write(struct.pack(self.endian + "b", int(bool_)))

    def write_byte(self, byte: int):
        self.buf.write(struct.pack(self.endian + "b", byte))

    def write_ubyte(self, ubyte: int):
        self.buf.write(struct.pack(self.endian + "B", ubyte))

    def write_int16(self, int16: int):
        self.buf.write(struct.pack(self.endian + "h", int16))

    def write_uint16(self, uint16: int):
        self.buf.write(struct.pack(self.endian + "H", uint16))

    def write_int32(self, int32: int):
        self.buf.write(struct.pack(self.endian + "i", int32))

    def write_uint32(self, uint32: int):
        self.buf.write(struct.pack(self.endian + "I", uint32))

    def write_int64(self, int64: int):
        self.buf.write(struct.pack(self.endian + "q", int64))

    def write_uint64(self, uint64: int):
        self.buf.write(struct.pack(self.endian + "Q", uint64))

    def write_float(self, float_: float):
        self.buf.write(struct.pack(self.endian + "f", float_))

    def write_double(self, double_: float):
        self.buf.write(struct.pack(self.endian + "d", double_))

    def write_bytearray(self, bytearray_: bytearray):
        self.buf.write(bytearray_)

    def close(self):
        self.buf.close()

    def length(self):
        t = self.buf.tell()
        self.buf.seek(0, SEEK_END)
        length = self.buf.tell()
        self.buf.seek(t)
        return length
