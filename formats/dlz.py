import struct
from typing import BinaryIO

from formats.binary import BinaryReader, BinaryWriter
from formats.filesystem import FileFormat


class Dlz(FileFormat):
    """
    DLZ file format on the Layton ROM.

    Each DLZ file consists of a binary structure repeated over and over.
    """
    _entries = list[bytes]

    _compressed_default = 1

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        n_entries = rdr.read_uint16()
        header_length = rdr.read_uint16()
        entry_length = rdr.read_uint16()
        rdr.seek(header_length)

        self._entries = []

        for i in range(n_entries):
            self._entries.append(rdr.read(entry_length))

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

    def unpack(self, __format: str):
        """
        Unpack the entries in the DLZ file according to a struct format.

        Parameters
        ----------
        __format : str
            The format of each entry as a `struct` module format.

        Returns
        -------
        List[Tuple]
            A list containing all the unpacked entries.
        """
        return [struct.unpack(__format, entry) for entry in self._entries]

    def pack(self, fmt, data: list):
        """
        Pack the supplied data entries according to a struct format.

        Parameters
        ----------
        fmt : str
            The format of each entry as a `struct` module format.
        data : List[Tuple]
            A list of the entries.

            Is entry is a structure following the format specified in the fmt parameter.
        """
        self._entries = [struct.pack(fmt, *entry_dat) for entry_dat in data]
