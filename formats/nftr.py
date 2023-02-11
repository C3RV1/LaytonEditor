# http://problemkaputt.de/gbatek.htm#dscartridgenitrofontresourceformat
from typing import List, Dict, Tuple

import numpy

from formats.filesystem import FileFormat
from formats.binary import BinaryReader, BinaryWriter
import numpy as np


class NFTRHeader:
    """
    A class representing the data of the header chunk of a NFTR file.
    """
    magic_value: bytes = b"RTFN"
    byte_order: int = 0xFEFF
    version: int  # 0x100 to 0x102
    file_size: int  # 0x000A3278
    offset_to_fnif: int  # Offset to the FNIF chunk or size of the NFTR header
    following_chunk_count: int  # 3 + char map count

    def read(self, rdr: BinaryReader):
        self.magic_value = rdr.read(4)[::-1]
        if self.magic_value != b"NFTR":
            raise ValueError("NFTRHeader does not start with magic value")
        self.byte_order = rdr.read_uint16()
        self.version = rdr.read_uint16()
        self.file_size = rdr.read_uint32()
        self.offset_to_fnif = rdr.read_uint16()
        self.following_chunk_count = rdr.read_uint16()

    def write(self, wtr: BinaryWriter, chunk_count: int):
        wtr.write(b"NFTR"[::-1])
        wtr.write_uint16(0xFEFF)
        wtr.write_uint16(0x100)  # TODO: Version 0x102
        file_size_pos = wtr.tell()
        wtr.write_uint32(0)  # placeholder file size
        wtr.write_uint16(0x10)
        wtr.write_uint16(chunk_count)
        return file_size_pos


class FINFChunk:
    """
    Font INFo chunk on a NFTR file.
    """
    chunk_id: bytes = b"FINF"
    chunk_size: int  # 0x1C if version < 0x102 else 0x20
    height: int
    unk0: int  # usually 00 sometimes 1F
    width: int
    encoding: int
    offset_to_cglp_chunk: int
    offset_to_cwdh_chunk: int
    offset_to_cmap_chunk: int

    def read(self, rdr: BinaryReader):
        self.chunk_id = rdr.read(4)[::-1]
        if self.chunk_id != b"FINF":
            raise ValueError("FINFChunk does not start with magic value")
        self.chunk_size = rdr.read_uint32()
        rdr.read(1)
        self.height = rdr.read_uint8()
        self.unk0 = rdr.read_uint8()
        rdr.read(2)
        self.width = rdr.read_uint8()
        rdr.read(1)  # Width bis or width + 1?
        self.encoding = rdr.read_uint8()
        self.offset_to_cglp_chunk = rdr.read_uint32() - 8
        self.offset_to_cwdh_chunk = rdr.read_uint32() - 8
        self.offset_to_cmap_chunk = rdr.read_uint32() - 8
        rdr.read(self.chunk_size - 0x1C)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"FINF"[::-1])
        wtr.write_uint32(0x1C)
        wtr.write_uint8(0)
        wtr.write_uint8(self.height)
        wtr.write_uint8(self.unk0)
        wtr.write_uint16(0)
        wtr.write_uint8(self.width)
        wtr.write_uint8(self.width)
        wtr.write_uint8(self.encoding)
        offset_to_cglp_pos = wtr.tell()
        wtr.write_uint32(0)
        offset_to_cwdh_pos = wtr.tell()
        wtr.write_uint32(0)
        offset_to_cmap_pos = wtr.tell()
        wtr.write_uint32(0)
        return offset_to_cglp_pos, offset_to_cwdh_pos, offset_to_cmap_pos


def get_max_bit_steps(depth: int) -> int:
    """
    Used to determine how bits we can read at a time so as to line up with a byte for a certain bit depth.

    In fact, gets the value of the first 1 in binary representation.

    Examples
    --------

    >>> get_max_bit_steps(1)
    1, because the binary is 0b1. We read one bit at a time.

    >>> get_max_bit_steps(2)
    2, because the binary is 0b10.
    We can read 2 bits at a time and still align with a byte (aabbccdd eeffgghh: a value never lands between 2 bytes).

    >>> get_max_bit_steps(3)
    1, because the binary is 0b11, and the first 1 from the left is 0b1.
    We can read 1 but at a time and still align with a byte (aaabbbcc cdddeeef ffggghhh, the last c is "alone").

    >>> get_max_bit_steps(6)
    2, because the binary is 0b110 and the first 1 from the left is 0b10.
    We can read 2 bytes at a time and still align with a byte (aaaaaabb bbbbcccc ccdddddd, max "block" size is 2 bits).

    Parameters
    ----------
    depth:
        The bit depth for which to calculate the maximum bit steps.

    Returns
    -------
    int
        The numbers of bits that can be read at a time for the specified bit depth and still align with the bytes.
    """
    if depth == 0:
        return 0
    bit_steps = 1
    while not depth & 0x1:
        bit_steps <<= 1
        depth >>= 1
    return bit_steps


class CGLPChunk:
    """
    Character GLyPh chunk on a NFTR file.
    """
    chunk_id: bytes = b"CGLP"
    chunk_size: int  # 10 + tile_count * size + padding
    tile_width: int
    tile_height: int
    tile_bytes: int  # (width * height * bpp + 7) / 8
    underline_location: int
    max_proportional_width: int
    tile_depth: int  # Bits per pixel
    tile_rotation: int
    tile_bitmaps: List[np.ndarray]

    def read(self, rdr: BinaryReader):
        self.chunk_id = rdr.read(4)[::-1]
        if self.chunk_id != b"CGLP":
            raise ValueError("CGLPChunk does not start with magic value")
        self.chunk_size = rdr.read_uint32()
        self.tile_width = rdr.read_uint8()
        self.tile_height = rdr.read_uint8()
        self.tile_bytes = rdr.read_uint16()
        bitmap_items = self.tile_width * self.tile_height
        self.underline_location = rdr.read_uint8()
        self.max_proportional_width = rdr.read_uint8()
        self.tile_depth = rdr.read_uint8()
        self.tile_rotation = rdr.read_uint8()

        self.tile_bitmaps = []

        tile_bytes = self.tile_bytes
        tile_width = self.tile_width
        tile_height = self.tile_height
        tile_depth = self.tile_depth
        # To always land in byte boundaries:
        # If bit depth is 2, we can read in blocks of 2 bits
        # If bit depth is 1, we can only read in blocks of 1 bit
        # If bit depth is 3, we can only read in blocks of 1 bit
        # If bit depth is 4, we can read in blocks of 4 bits
        # ...
        bit_steps = get_max_bit_steps(self.tile_depth)
        bit_mask = ((1 << bit_steps) - 1)

        for _ in range((self.chunk_size - 0x10) // tile_bytes):
            buffer = rdr.read(tile_bytes)
            bitmap = np.zeros(bitmap_items, dtype=np.uint8)

            current_bit = 0
            for i in range(bitmap_items):
                # Get value from bytes to bit depth
                v = 0
                for _ in range(tile_depth // bit_steps):
                    # Shift the value bit steps
                    v <<= bit_steps

                    # Get the bit index and the byte index
                    bit_i = current_bit % 8
                    byte_i = (current_bit - bit_i) // 8

                    # Read <bit steps> bits from byte (bit 7 is the MSB)
                    byte = buffer[byte_i]
                    bit = (byte >> (7 - bit_i)) & bit_mask

                    # Add the value and change the current bit
                    v += bit
                    current_bit += bit_steps

                bitmap[i] = v

            bitmap.shape = tile_height, tile_width
            self.tile_bitmaps.append(bitmap)

    def write(self, wtr: BinaryWriter):
        chunk_start = wtr.tell()
        wtr.write(b"CGLP"[::-1])
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)
        wtr.write_uint8(self.tile_width)
        wtr.write_uint8(self.tile_height)
        tile_bytes = (self.tile_width * self.tile_height * self.tile_depth + 7) // 8
        wtr.write_uint16(tile_bytes)

        wtr.write_uint8(self.underline_location)
        wtr.write_uint8(self.max_proportional_width)
        wtr.write_uint8(self.tile_depth)
        wtr.write_uint8(self.tile_rotation)

        bitmap_items = self.tile_width * self.tile_height

        # TODO: optimize bitmap saving as with loading
        for bitmap in self.tile_bitmaps:
            bitmap = bitmap.copy()
            bitmap.shape = bitmap_items,

            buffer = [0] * tile_bytes

            current_bit = 0
            for i in range(bitmap_items):
                value = bitmap[i]
                for bit in range(self.tile_depth):
                    bit_value = (value >> (self.tile_depth - bit - 1)) & 1

                    bit_i = current_bit % 8
                    byte_i = (current_bit - bit_i) // 8

                    buffer[byte_i] += bit_value << (7 - bit_i)
                    current_bit += 1

            wtr.write(bytes(buffer))

        wtr.align(4)
        chunk_end = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(chunk_end - chunk_start)
        wtr.seek(chunk_end)


class CWDHChunk:  # Character width
    """
    Character WiDtH chunk on a NTFR file.
    """
    chunk_id: bytes = b"CWDH"
    chunk_size: int  # 0x10 + tile_count*3 + padding
    first_tile_no: int = 0
    last_tile_no: int  # tile_count - 1
    left_spacing: List[int]
    width: List[int]
    total_width: List[int]

    def read(self, rdr: BinaryReader, tile_count: int):
        self.chunk_id = rdr.read(4)[::-1]
        if self.chunk_id != b"CWDH":
            raise ValueError("CWDHChunk does not start with magic value")
        self.chunk_size = rdr.read_uint32()
        self.first_tile_no = rdr.read_uint16()
        self.last_tile_no = rdr.read_uint16()
        rdr.read(4)

        self.left_spacing = []
        self.width = []
        self.total_width = []
        for i in range(tile_count):
            left_spacing = rdr.read_uint8()
            width = rdr.read_uint8()
            total_width = rdr.read_uint8()

            self.left_spacing.append(left_spacing)
            self.width.append(width)
            self.total_width.append(total_width)

    def write(self, wtr: BinaryWriter, tile_count: int):
        chunk_start = wtr.tell()
        wtr.write(b"CWDH"[::-1])
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)
        wtr.write_uint16(0)
        wtr.write_uint16(tile_count - 1)
        wtr.write_uint32(0)
        for i in range(tile_count):
            wtr.write_uint8(self.left_spacing[i])
            wtr.write_uint8(self.width[i])
            wtr.write_uint8(self.total_width[i])
        wtr.align(4)

        chunk_end = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(chunk_end - chunk_start)
        wtr.seek(chunk_end)


class CMAPChunk:
    """
    Character MAP chunk on a NFTR file.
    """
    chunk_id: bytes  # CMAP
    chunk_size: int
    first_character: int
    last_character: int
    map_type: int
    offset_to_next_cmap: int

    char_map: Dict[int, int]

    def read(self, rdr: BinaryReader):
        self.chunk_id = rdr.read(4)[::-1]
        if self.chunk_id != b"CMAP":
            raise ValueError("CMAPChunk does not start with magic value")
        self.chunk_size = rdr.read_uint32()
        self.first_character = rdr.read_uint16()
        self.last_character = rdr.read_uint16()
        self.map_type = rdr.read_uint32()
        self.offset_to_next_cmap = rdr.read_uint32() - 8

        char_map = {}
        if self.map_type == 0:
            tile_no = rdr.read_uint16()
            i = self.first_character
            while i <= self.last_character:
                char_map[i] = tile_no
                i += 1
                tile_no += 1
        elif self.map_type == 1:
            i = self.first_character
            while i <= self.last_character:
                tile = rdr.read_uint16()
                if tile == 0xFFFF:
                    i += 1
                    continue
                char_map[i] = tile
                i += 1
        elif self.map_type == 2:
            groups = rdr.read_uint16()
            for i in range(groups):
                ch = rdr.read_uint16()
                tile = rdr.read_uint16()
                char_map[ch] = tile
        self.char_map = char_map

    def write(self, wtr: BinaryWriter):
        chunk_start = wtr.tell()
        wtr.write(b"CMAP"[::-1])
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)

        characters: List[Tuple] = list(self.char_map.items())
        if len(characters) == 0:
            raise ValueError()
        characters.sort(key=lambda x: x[0])
        first, last = characters[0], characters[-1]

        ch_increasing = True
        tile_increasing = True
        for i, (ch, tile) in enumerate(characters[:-1]):
            next_ch, next_tile = characters[i + 1]
            if ch != next_ch - 1:
                ch_increasing = False
                break
            elif tile != next_tile - 1:
                tile_increasing = False

        if ch_increasing and tile_increasing:
            map_type = 0
        else:
            map_type_1_len = last[0] - first[0] + 1
            map_type_2_len = len(characters) * 2
            if map_type_2_len < map_type_1_len:
                map_type = 2
            else:
                map_type = 1

        if map_type == 0 or map_type == 1:
            wtr.write_uint16(first[0])
            wtr.write_uint16(last[0])
        else:
            wtr.write_uint16(0)
            wtr.write_uint16(0xFFFF)

        wtr.write_uint32(map_type)
        offset_to_next_cmap_pos = wtr.tell()
        wtr.write_uint32(0)

        if map_type == 0:
            wtr.write_uint16(characters[0][1])
        elif map_type == 1:
            for ch in range(first[0], last[0] + 1):
                wtr.write_uint16(self.char_map.get(ch, 0xFFFF))
        else:
            wtr.write_uint16(len(characters))
            for ch, tile in characters:
                wtr.write_uint16(ch)
                wtr.write_uint16(tile)

        wtr.align(4)

        chunk_end = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(chunk_end - chunk_start)
        wtr.seek(chunk_end)

        return offset_to_next_cmap_pos


class NFTR(FileFormat):
    """
    Nitro FonT Resource file format.
    """
    header: NFTRHeader
    font_info: FINFChunk
    char_glyph: CGLPChunk
    char_width: CWDHChunk
    char_maps: List[CMAPChunk]

    def read_stream(self, stream: any):
        if isinstance(stream, BinaryReader):
            rdr: BinaryReader = stream
        else:
            rdr: BinaryReader = BinaryReader(stream)
        self.header = NFTRHeader()
        self.font_info = FINFChunk()
        self.char_glyph = CGLPChunk()
        self.char_width = CWDHChunk()
        self.char_maps = []

        self.header.read(rdr)

        rdr.seek(self.header.offset_to_fnif)
        self.font_info.read(rdr)

        rdr.seek(self.font_info.offset_to_cglp_chunk)
        self.char_glyph.read(rdr)

        rdr.seek(self.font_info.offset_to_cwdh_chunk)
        self.char_width.read(rdr, len(self.char_glyph.tile_bitmaps))

        next_offset = self.font_info.offset_to_cmap_chunk
        for i in range(self.header.following_chunk_count - 3):
            rdr.seek(next_offset)
            cmap = CMAPChunk()
            cmap.read(rdr)
            self.char_maps.append(cmap)
            next_offset = cmap.offset_to_next_cmap

    def write_stream(self, stream: any):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        file_size_pos = self.header.write(wtr, 3 + len(self.char_maps))
        offset_to_cglp_pos, offset_to_cwdh_pos, offset_to_cmap_pos = self.font_info.write(wtr)

        def write_pos_seek_back(wtr_pos, add=0):
            pos = wtr.tell()
            wtr.seek(wtr_pos)
            wtr.write_uint32(pos + add)
            wtr.seek(pos)

        write_pos_seek_back(offset_to_cglp_pos, add=8)
        self.char_glyph.write(wtr)

        write_pos_seek_back(offset_to_cwdh_pos, add=8)
        self.char_width.write(wtr, len(self.char_glyph.tile_bitmaps))

        cmap_wtr_pos = offset_to_cmap_pos
        for cmap_chunk in self.char_maps:
            write_pos_seek_back(cmap_wtr_pos, add=8)
            cmap_wtr_pos = cmap_chunk.write(wtr)

        write_pos_seek_back(file_size_pos)

        # Match file size after alignment
        if len(wtr.getvalue()) != wtr.tell():
            wtr.seek(wtr.tell() - 1)
            wtr.write(b"\0")

    def get_encoding_str(self):
        encoding_dict = {
            0: "utf8",
            1: "unicode",
            2: "shift-jis",
            3: "cp1252"
        }
        return encoding_dict[self.font_info.encoding]
