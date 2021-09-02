# http://problemkaputt.de/gbatek.htm#dscartridgenitrofontresourceformat
from typing import List, Dict

from formats.filesystem import FileFormat
from formats.binary import BinaryReader
import numpy as np


class NFTRHeader:
    magic_value: bytes  # b"RTFN"
    byte_order: int  # 0xFEFF
    version: int  # 0x100 to 0x102
    decompressed_resource_size: int  # 0x000A3278
    offset_to_fnif: int  # Offset to the FNIF chunk or size of the NFTR header
    following_chunk_count: int  # 3 + char map count

    def read(self, rdr: BinaryReader):
        self.magic_value = rdr.read(4)[::-1]
        if self.magic_value != b"NFTR":
            raise ValueError("NFTRHeader does not start with magic value")
        self.byte_order = rdr.read_uint16()
        self.version = rdr.read_uint16()
        self.decompressed_resource_size = rdr.read_uint32()
        self.offset_to_fnif = rdr.read_uint16()
        self.following_chunk_count = rdr.read_uint16()


class FINFChunk:  # Font Info
    chunk_id: bytes  # FINF
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
        rdr.read(1)  # Width bis
        self.encoding = rdr.read_uint8()
        self.offset_to_cglp_chunk = rdr.read_uint32() - 8
        self.offset_to_cwdh_chunk = rdr.read_uint32() - 8
        self.offset_to_cmap_chunk = rdr.read_uint32() - 8
        rdr.read(self.chunk_size - 0x1C)


def get_bit_steps(depth: int) -> int:
    if depth == 0:
        return 0
    bit_steps = 1
    while not depth & 0x1:
        bit_steps <<= 1
        depth >>= 1
    return bit_steps


class CGLPChunk:  # Character Glyph
    chunk_id: bytes  # CGLP
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
        # To avoid byte boundaries efficiently
        # If bit depth is 2, we can read in blocks of 2
        # If bit depth is 1, we can only read in blocks of 1
        bit_steps = get_bit_steps(self.tile_depth)
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


class CWDHChunk:  # Character width
    chunk_id: bytes  # CWDH
    chunk_size: int  # 0x10 + tile_count*3 + padding
    first_tile_no: int  # 0
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


class CMAPChunk:
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


class NFTR(FileFormat):
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

    def get_encoding_str(self):
        encoding_dict = {
            0: "utf8",
            1: "unicode",
            2: "shift-jis",
            3: "cp1252"
        }
        return encoding_dict[self.font_info.encoding]

    def write_stream(self, stream):
        raise NotImplementedError("NTFR Saving not implemented")
