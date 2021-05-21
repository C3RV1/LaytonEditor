from dataclasses import dataclass, field
from typing import BinaryIO
from typing import List, Union

from formats.binary import BinaryReader, BinaryWriter
from formats.filesystem import FileFormat


@dataclass
class GDSCommand:
    command: int
    params: List[Union[int, float, str]] = field(default_factory=list)


class GDS(FileFormat):
    params: List[Union[int, float, str]] = []
    commands: List[GDSCommand] = []

    _compressed_default = False

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        self.commands = []
        self.params = []
        file_length = rdr.read_uint32()

        while rdr.c < file_length:
            datatype = rdr.read_uint16()
            if datatype == 0:
                break
            elif datatype == 1:
                self.params.append(rdr.read_uint32())
            elif datatype == 2:
                self.params.append(rdr.read_float())
            elif datatype == 3:
                self.params.append(rdr.read_string(rdr.read_uint16()))
            elif datatype == 0xc:
                return
        while rdr.c < file_length:
            self.commands.append(command := GDSCommand(rdr.read_uint16()))
            while rdr.c < file_length:
                datatype = rdr.read_uint16()
                if datatype == 0:
                    break
                elif datatype == 1:
                    command.params.append(rdr.read_uint32())
                elif datatype == 2:
                    command.params.append(rdr.read_float())
                elif datatype == 3:
                    command.params.append(rdr.read_string(rdr.read_uint16()))
                elif datatype == 0xc:
                    return

    def write_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)
        wtr.write_uint32(0)  # placeholder for file length
        for p in self.params:
            if isinstance(p, int):
                wtr.write_uint16(1)
                wtr.write_uint32(p)
            elif isinstance(p,float):
                wtr.write_uint16(2)
                wtr.write_float(p)
            elif isinstance(p, str):
                wtr.write_uint16(3)
                wtr.write_uint16(len(p)+1)
                wtr.write_string(p)
                wtr.write_uint8(0)
        for c in self.commands:
            wtr.write_uint16(0)
            wtr.write_uint16(c.command)
            for p in c.params:
                if isinstance(p, int):
                    wtr.write_uint16(1)
                    wtr.write_uint32(p)
                elif isinstance(p, float):
                    wtr.write_uint16(2)
                    wtr.write_float(p)
                elif isinstance(p, str):
                    wtr.write_uint16(3)
                    wtr.write_uint16(len(p)+1)
                    wtr.write_string(p)
                    wtr.write_uint8(0)
        wtr.write_uint16(0xc)
        wtr.seek(0)
        wtr.write_uint32(len(wtr.data) - 4)
