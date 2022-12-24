import logging
from typing import *
import ndspy.lz10 as lz10
from formats.compression import rle, huffman
import struct

# Compression containers
LZ10 = 0x10
RLE = 0x30
HUFF8BIT = 0x28
HUFF4BIT = 0x24

SECOND_TYPES = {
    RLE: 1,
    LZ10: 2,
    HUFF4BIT: 3,
    HUFF8BIT: 4
}


def compress(data: bytes, compression_type=LZ10, double_typed: bool = None) -> bytes:
    if not data:
        return b""
    if double_typed is None:
        logging.warning("Compressing file without knowing if it's double typed, defaulting to not.")
        double_typed = False
    other_type = struct.pack("<I", SECOND_TYPES[compression_type]) if double_typed else b""
    if compression_type == LZ10:
        return other_type + lz10.compress(data)
    elif compression_type == RLE:
        return other_type + rle.compress(data)
    elif compression_type == HUFF8BIT:
        return other_type + huffman.compress(data, 8)
    elif compression_type == HUFF4BIT:
        return other_type + huffman.compress(data, 4)
    else:
        raise NotImplementedError(f"compression type: {hex(compression_type)}")


def decompress(data: bytes, double_typed: bool = None) -> Tuple[bytes, bool]:
    if not data:
        return b"", double_typed
    if double_typed is None:
        first_word = struct.unpack("<I", data[:4])
        double_typed = first_word in SECOND_TYPES.values()
    if double_typed:
        data = data[4:]
    compression_type = data[0]
    if compression_type == LZ10:
        ret = lz10.decompress(data), double_typed
        return ret
    elif compression_type == RLE:
        return rle.decompress(data), double_typed
    elif compression_type in [HUFF8BIT, HUFF4BIT]:
        return huffman.decompress(data), double_typed
    else:
        raise NotImplementedError(f"compression type: {hex(compression_type)}")
