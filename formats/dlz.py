import logging
import struct
from typing import BinaryIO, Dict

from formats.binary import BinaryReader, BinaryWriter
from formats.filesystem import FileFormat
from abc import ABC


class Dlz(FileFormat, ABC, dict):
    """
    Dictionary format in the Layton2 game.
    Each key is an ushort.
    Each value is a structure.

    They are sorted in the file, because the game uses
    a binary search to look for the specified value.
    """
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

        self.clear()

        for i in range(n_entries):
            entry_id = rdr.read_uint16()
            entry_data = rdr.read(entry_length - 2)
            if entry_id in self:
                logging.warning(f"Duplicate value ({entry_id}) in {self._last_filename}, ignoring")
                continue
            self[entry_id] = self._construct_entry_object(entry_data)

    def _construct_entry_object(self, entry_data: bytes) -> object:
        """Derived classes must implement"""
        pass

    def _serialize_entry_object(self, entry_object: object) -> bytes:
        """Derived classes must implement"""
        pass

    def write_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint16(len(self))
        wtr.write_uint16(8)
        size_pos = wtr.tell()
        global_entry_size = None
        wtr.write_uint16(0)
        wtr.write_uint16(0)

        entries = list(self.values())
        entries.sort(key=lambda x: x[0])
        for entry_id, entry_object in entries:
            wtr.write_uint16(entry_id)

            entry_data = self._serialize_entry_object(entry_object)
            entry_size = len(entry_data) + 2

            if global_entry_size is None:
                global_entry_size = entry_size

                pos = wtr.tell()
                wtr.seek(size_pos)
                wtr.write_uint16(global_entry_size)
                wtr.seek(pos)
            elif entry_size != global_entry_size:
                raise ValueError(f"All serialized objects should be of the same size in {self._last_filename}")

            wtr.write(entry_data)
