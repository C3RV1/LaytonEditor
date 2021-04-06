# FROM: https://github.com/jleclanche/binreader
# Modified by Cervi

import struct
from os import SEEK_CUR, SEEK_END
from typing import BinaryIO

ENDIAN_PREFIXES = ("@", "<", ">", "=", "!")


class BinaryReader:
    def __init__(self, buf: BinaryIO, endian: str = "<") -> None:
        self.buf = buf
        self.endian = endian

    def align(self) -> None:
        old = self.tell()
        new = (old + 3) & -4
        if new > old:
            self.seek(new - old, SEEK_CUR)

    def read(self, *args) -> bytes:
        return self.buf.read(*args)

    def seek(self, *args) -> int:
        return self.buf.seek(*args)

    def tell(self) -> int:
        return self.buf.tell()

    def read_string(self, size: int = None, encoding: str = "utf-8") -> str:
        if size is None:
            ret = self.read_cstring()
        else:
            ret = struct.unpack(self.endian + "%is" % size, self.read(size))[0]

        return ret.decode(encoding)

    def read_cstring(self) -> bytes:
        ret = []
        c = b""
        while c != b"\0":
            ret.append(c)
            c = self.read(1)
            if not c:
                raise ValueError("Unterminated string: %r" % ret)
        return b"".join(ret)

    def read_bool(self) -> bool:
        return bool(struct.unpack(self.endian + "b", self.read(1))[0])

    def read_byte(self) -> int:
        return struct.unpack(self.endian + "b", self.read(1))[0]

    def read_ubyte(self) -> int:
        return struct.unpack(self.endian + "B", self.read(1))[0]

    def read_int16(self) -> int:
        return struct.unpack(self.endian + "h", self.read(2))[0]

    def read_uint16(self) -> int:
        return struct.unpack(self.endian + "H", self.read(2))[0]

    def read_int32(self) -> int:
        return struct.unpack(self.endian + "i", self.read(4))[0]

    def read_uint32(self) -> int:
        return struct.unpack(self.endian + "I", self.read(4))[0]

    def read_int64(self) -> int:
        return struct.unpack(self.endian + "q", self.read(8))[0]

    def read_uint64(self) -> int:
        return struct.unpack(self.endian + "Q", self.read(8))[0]

    def read_float(self) -> float:
        return struct.unpack(self.endian + "f", self.read(4))[0]

    def read_double(self) -> float:
        return struct.unpack(self.endian + "d", self.read(8))[0]

    def read_struct(self, format_: str) -> tuple:
        if not format_.startswith(ENDIAN_PREFIXES):
            format_ = self.endian + format_
        size = struct.calcsize(format_)
        return struct.unpack(format_, self.read(size))

    # Aliases

    def read_int(self) -> int:
        return self.read_int32()

    def read_uint(self) -> int:
        return self.read_uint32()

    # Missing

    def read_chars(self, count: int) -> bytes:
        # 2 bytes per char
        return self.buf.read(count)

    def read_bytearray(self, count: int) -> bytearray:
        return bytearray(self.buf.read(count))

    def close(self):
        self.buf.close()

    def length(self):
        t = self.buf.tell()
        self.buf.seek(0, SEEK_END)
        length = self.buf.tell()
        self.buf.seek(t)
        return length
