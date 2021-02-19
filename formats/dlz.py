import struct
from typing import BinaryIO, List

from formats.binary import BinaryReader, BinaryWriter
from formats.filesystem import FileFormat


class Dlz(FileFormat):
    entries = List[bytes]

    _compressed_default = True

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        n_entries = rdr.read_uint16()
        header_lenght = rdr.read_uint16()
        entry_lenght = rdr.read_uint16()
        rdr.seek(header_lenght)

        for i in range(n_entries):
            self._entries.append(rdr.read(entry_lenght))

    def write_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint16(len(self._entries))
        wtr.write_uint16(8)
        wtr.write_uint16(len(self._entries[0]))
        wtr.write_uint16(0)

        for entry in self._entries:
            wtr.write(entry)

    def unpack(self, __format):
        return [struct.unpack(__format, entry) for entry in self._entries]

    def pack(self, fmt, data: list):
        self._entries = [struct.pack(fmt, entry_dat) for entry_dat in data]
