from formats.filesystem import FileFormat
from enum import IntEnum
from formats.binary import BinaryReader, BinaryWriter
from typing import BinaryIO


class PlaceFlagComparator(IntEnum):
    EQUALS = 0
    NOT_EQUALS = 1
    LESS_THAN = 2


class PlaceFlagVersion:
    """
    Represents a version in the PlaceFlag file.
    The Entry is divided in two parts:
    - Part 1 (first 0x2000 bytes of the file)
      - Lower bound (short)
      - Upper bound (short)
    - Part 2 (following 0x1800 bytes of the file)
      - Place flag id to check
      - Comparator
      - Check Value
    """

    def __init__(self, lower_bound=0, upper_bound=0, place_flag_id=0,
                 comparator=PlaceFlagComparator.EQUALS, check_value=0):
        self.lower_bound: int = lower_bound
        self.upper_bound: int = upper_bound

        self.place_flag_id: int = place_flag_id
        self.comparator: PlaceFlagComparator = comparator
        self.check_value = check_value

    def read_part1(self, rdr: BinaryReader):
        self.lower_bound = rdr.read_uint16()
        self.upper_bound = rdr.read_uint16()

    def read_part2(self, rdr: BinaryReader):
        self.place_flag_id = rdr.read_uint8()
        comparator = rdr.read_uint8()
        if not 0 <= comparator <= 2:
            raise ValueError(f"Unknown comparator value ({comparator})")
        self.comparator = PlaceFlagComparator(comparator)
        self.check_value = rdr.read_uint8()

    def write_part1(self, wtr: BinaryWriter):
        # For version 0 is 0, 0
        wtr.write_uint16(self.lower_bound)
        wtr.write_uint16(self.upper_bound)

    def write_part2(self, wtr: BinaryWriter):
        # For version 0 is 0, 0, 0
        wtr.write_uint8(self.place_flag_id)
        if not 0 <= self.comparator <= 2:
            raise ValueError(f"Unknown comparator value ({self.comparator})")
        wtr.write_uint8(self.comparator)
        wtr.write_uint8(self.check_value)

    def __repr__(self):
        range_str = f"range=[{self.lower_bound}, {self.upper_bound}]"
        if self.lower_bound == 0 and self.upper_bound == 0:
            range_str = "default"

        if self.place_flag_id != 0:
            comparator_str = {
                PlaceFlagComparator.EQUALS: "==",
                PlaceFlagComparator.NOT_EQUALS: "!=",
                PlaceFlagComparator.LESS_THAN: "<="
            }[self.comparator]
            return f"PlaceVersion<{range_str}, " \
                   f"place_flag {self.place_flag_id} {comparator_str} {self.check_value}>"
        else:
            return f"PlaceVersion<{range_str}>"


class PlaceFlagPlace(list):

    def read_part1(self, rdr: BinaryReader, place_id: int):
        rdr.seek(place_id * 0x40)
        for i in range(16):
            version = PlaceFlagVersion()
            version.read_part1(rdr)
            if version.lower_bound == 0 and version.upper_bound == 0 and i != 0:  # Version 0 must(?) have range [0, 0]
                return
            self.append(version)

    def read_part2(self, rdr: BinaryReader, place_id: int):
        rdr.seek(0x2000 + place_id * 0x30)
        for version in self:
            version: PlaceFlagVersion
            version.read_part2(rdr)

    def write_part1(self, wtr: BinaryWriter, place_id: int):
        wtr.seek(place_id * 0x40)
        if len(self) > 16:
            raise ValueError("PlaceFlagPlace cannot have more than 16 versions")
        for version in self:
            version: PlaceFlagVersion
            version.write_part1(wtr)

    def write_part2(self, wtr: BinaryWriter, place_id: int):
        wtr.seek(0x2000 + place_id * 0x30)
        if len(self) > 16:
            raise ValueError("PlaceFlagPlace cannot have more than 16 versions")
        for version in self:
            version: PlaceFlagVersion
            version.write_part2(wtr)
        for _ in range(16 - len(self)):
            version = PlaceFlagVersion()
            version.write_part2(wtr)


class PlaceFlag(FileFormat, list):
    def read_stream(self, stream):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        self.clear()

        # Read first part
        for i in range(128):
            place = PlaceFlagPlace()
            self.append(place)
            place.read_part1(rdr, i)

        # Read second part
        for i, place in enumerate(self):
            place: PlaceFlagPlace
            place.read_part2(rdr, i)

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        if len(self) != 128:
            raise ValueError("PlaceFlag must have 128 places.")

        # Write first part
        for i, place in enumerate(self):
            place: PlaceFlagPlace
            place.write_part1(wtr, i)

        # Write second part
        for i, place in enumerate(self):
            place: PlaceFlagPlace
            place.write_part2(wtr, i)
