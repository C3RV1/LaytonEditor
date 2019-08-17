import ndspy.rom as nr
import ndspy.lz10 as lz10
from ndspy.fnt import Folder

LZ10 = 0x10

def decompress(data: bytes):
    if int(data[0]) == 16:
        return lz10.decompress(data)
    else:
        raise Exception("Unsupported compression type with starting byte %s" % hex(data[0]))

def compress(data: bytes, type):
    if type == 0x10:
        return lz10.compress(data)
    else:
        raise Exception("Unsupported compression type with starting byte %s" % type)

class NDS(nr.NintendoDSRom):
    pass